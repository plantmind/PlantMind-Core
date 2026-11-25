"""RFC-082 optional ingestion in the existing canonical platform graph."""

from __future__ import annotations

from collections.abc import Sequence
from inspect import Parameter, signature
from typing import get_type_hints
from unittest.mock import Mock

import pytest

from app.core.composition import composition_root as composition
from app.core.runtime_state import RuntimeState
from app.services.application_facade import (
    ApplicationFacade,
    ApplicationFacadeDocumentIngestionNotConfiguredError,
)
from app.services.orchestration.workflow import WorkflowStage
from app.services.parsed_document_knowledge_ingestion_application_service import (
    ParsedDocumentKnowledgeIngestionApplicationService as ParsedService,
)


FACTORIES = [
    pytest.param(composition.CompositionRoot.build, id="root"),
    pytest.param(composition.build_platform_composition, id="wrapper"),
]
DEPENDENCY = "parsed_document_knowledge_ingestion_service"


class RecordingParsedService(ParsedService):
    """Caller-owned canonical subtype; no parsing or persistence graph."""

    def __init__(self):
        self.requests = []
        self.result = object()

    def ingest(self, request):
        self.requests.append(request)
        return self.result

    def unexpected_lifecycle(self, *args, **kwargs):
        raise AssertionError("Composition must not own the supplied service lifecycle")

    start = stop = startup = shutdown = close = unexpected_lifecycle
    __call__ = __enter__ = __exit__ = unexpected_lifecycle


class FalseyParsedService(RecordingParsedService):
    def __init__(self):
        super().__init__()
        self.bool_calls = 0

    def __bool__(self):
        self.bool_calls += 1
        return False


class DuckService:
    def ingest(self, request):
        raise AssertionError("A noncanonical service must be rejected")


def assert_facade_identity(platform, service):
    facade = platform.application_facade
    assert isinstance(facade, ApplicationFacade)
    assert facade._parsed_document_knowledge_ingestion_service is service
    assert platform.container.resolve(ApplicationFacade) is facade
    assert platform.operational_transition_application_service.application_facade is facade
    assert (
        platform.operational_transition_application_service.operational_transition_coordinator
        is platform.operational_transition_coordinator
    )
    return facade


def assert_inactive(platform):
    assert platform.runtime.state is RuntimeState.CREATED
    assert platform.runtime.is_request_admission_enabled is False


@pytest.mark.parametrize("factory", FACTORIES)
def test_canonical_service_is_forwarded_to_the_single_composed_facade(factory):
    """TDD red target: both existing factories reject this missing keyword."""
    parser, writer = Mock(), Mock()
    service = ParsedService(parsing_service=parser, ingestion_service=writer)

    platform = factory(parsed_document_knowledge_ingestion_service=service)

    assert type(service) is ParsedService
    assert_facade_identity(platform, service)
    assert_inactive(platform)
    assert not platform.container.is_registered(ParsedService)
    parser.parse.assert_not_called()
    writer.ingest.assert_not_called()


@pytest.mark.parametrize("factory", FACTORIES)
def test_factory_signature_preserves_three_inputs_and_adds_one_keyword_only(factory):
    parameters = signature(factory).parameters
    old_names = (
        "plugin_registrations",
        "capability_availability_sources",
        "mandatory_capability_policy",
    )
    assert tuple(parameters) == (*old_names, DEPENDENCY)
    for name, default in zip(old_names, ((), (), None)):
        assert parameters[name].kind is Parameter.POSITIONAL_OR_KEYWORD
        assert parameters[name].default == default
    assert parameters[DEPENDENCY].kind is Parameter.KEYWORD_ONLY
    assert parameters[DEPENDENCY].default is None
    assert get_type_hints(factory) == {
        "plugin_registrations": Sequence[composition.PluginRegistration],
        "capability_availability_sources": Sequence[composition.CapabilityAvailabilitySource],
        "mandatory_capability_policy": composition.MandatoryCapabilityPolicy | None,
        DEPENDENCY: ParsedService | None,
        "return": composition.PlatformComposition,
    }


@pytest.mark.parametrize("factory", FACTORIES)
@pytest.mark.parametrize("explicit_none", [False, True], ids=["omitted", "explicit-none"])
def test_omitted_and_none_leave_the_composed_facade_unconfigured(factory, explicit_none):
    platform = factory(**({DEPENDENCY: None} if explicit_none else {}))
    facade = assert_facade_identity(platform, None)

    with pytest.raises(ApplicationFacadeDocumentIngestionNotConfiguredError):
        facade.ingest_document_knowledge(object())

    assert not platform.container.is_registered(ParsedService)
    assert_inactive(platform)


@pytest.mark.parametrize("factory", FACTORIES)
def test_existing_three_positional_inputs_remain_accepted(factory):
    policy = composition.MandatoryCapabilityPolicy(
        state=composition.MandatoryCapabilityPolicyState.UNCONFIGURED,
        required_capabilities=(),
    )
    service = RecordingParsedService()

    platform = factory((), (), policy, parsed_document_knowledge_ingestion_service=service)

    assert platform.mandatory_capability_policy is policy
    assert_facade_identity(platform, service)
    assert service.requests == []
    assert_inactive(platform)
    with pytest.raises(TypeError):
        factory((), (), policy, service)


@pytest.mark.parametrize("factory", FACTORIES)
@pytest.mark.parametrize("bad", [
    pytest.param(False, id="false"),
    pytest.param(0, id="zero"),
    pytest.param("", id="empty-string"),
    pytest.param(object(), id="object"),
    pytest.param(DuckService(), id="duck-service"),
    pytest.param(ParsedService, id="class-not-instance"),
])
def test_invalid_service_is_rejected_before_any_graph_or_plugin_activity(factory, bad, monkeypatch):
    activity = []

    def forbidden(*args, **kwargs):
        activity.append("graph construction or plugin processing")
        raise AssertionError("Type validation must precede platform construction")

    class UnreadPlugins:
        __iter__ = forbidden

    for name in (
        "ServiceContainer", "ConfigurationProvider", "LoggingProvider", "Runtime",
        "ServiceRegistry", "PluginRegistry", "PluginLifecycleManager", "HealthCapability",
        "CapabilityAvailabilityObserver", "MandatoryCapabilityPolicy",
        "MandatoryCapabilityCoverageEvaluator", "OperationalTransitionCoordinator",
        "BootstrapManager", "WorkflowExecutor", "OrchestrationService", "IntegrationGateway",
        "ApplicationFacade", "OperationalTransitionApplicationService", "PlatformComposition",
    ):
        monkeypatch.setattr(composition, name, forbidden)

    with pytest.raises(TypeError):
        factory(UnreadPlugins(), parsed_document_knowledge_ingestion_service=bad)

    assert activity == []


@pytest.mark.parametrize("factory", FACTORIES)
def test_falsey_canonical_subclass_is_retained_without_truth_value_evaluation(factory):
    service = FalseyParsedService()

    platform = factory(parsed_document_knowledge_ingestion_service=service)

    facade = assert_facade_identity(platform, service)
    assert service.requests == []
    request = object()
    assert facade.ingest_document_knowledge(request) is service.result
    assert len(service.requests) == 1 and service.requests[0] is request
    assert service.bool_calls == 0
    assert_inactive(platform)


@pytest.mark.parametrize("factory", FACTORIES)
def test_injection_adds_no_registration_construction_or_lifecycle_work(factory, monkeypatch):
    service = RecordingParsedService()
    registrations, registries = [], []
    original_register = composition.ServiceContainer.register_instance
    original_registry_init = composition.ServiceRegistry.__init__

    def record_registration(container, service_type, instance):
        registrations.append((container, service_type, instance))
        return original_register(container, service_type, instance)

    def record_registry(registry, *args, **kwargs):
        registries.append(registry)
        original_registry_init(registry, *args, **kwargs)

    def forbidden_construction(*args, **kwargs):
        raise AssertionError("Composition must reuse the caller's service")

    monkeypatch.setattr(composition.ServiceContainer, "register_instance", record_registration)
    monkeypatch.setattr(composition.ServiceRegistry, "__init__", record_registry)
    monkeypatch.setattr(ParsedService, "__init__", forbidden_construction)
    baseline = factory()
    baseline_types = [service_type for _, service_type, _ in registrations]
    baseline_registries = tuple(registries)
    registrations.clear()
    registries.clear()

    platform = factory(parsed_document_knowledge_ingestion_service=service)

    assert [service_type for _, service_type, _ in registrations] == baseline_types
    assert all(container is platform.container for container, _, _ in registrations)
    assert all(instance is not service for _, _, instance in registrations)
    assert len(registries) == len(baseline_registries)
    assert any(registry is baseline.registry for registry in baseline_registries)
    assert any(registry is platform.registry for registry in registries)
    assert not platform.container.is_registered(ParsedService)
    assert not platform.container.is_registered(RecordingParsedService)
    assert service.requests == []
    assert_facade_identity(platform, service)
    assert_inactive(baseline)
    assert_inactive(platform)


@pytest.mark.parametrize("factory", FACTORIES)
def test_separate_builds_own_separate_graphs_and_retain_explicitly_shared_service(factory):
    service = RecordingParsedService()
    left = factory(parsed_document_knowledge_ingestion_service=service)
    right = factory(parsed_document_knowledge_ingestion_service=service)
    default = factory()

    for field in ("application_facade", "runtime", "container"):
        assert len({id(getattr(platform, field)) for platform in (left, right, default)}) == 3
    assert_facade_identity(left, service)
    assert_facade_identity(right, service)
    assert_facade_identity(default, None)
    assert service.requests == []
    for platform in (left, right, default):
        assert_inactive(platform)


@pytest.mark.parametrize("factory", FACTORIES)
def test_injected_facade_keeps_existing_analysis_graph_and_runtime_state(factory):
    service = RecordingParsedService()
    platform = factory(parsed_document_knowledge_ingestion_service=service)
    assert platform.application_facade._gateway is platform.integration_gateway
    assert platform.integration_gateway._orchestration_service is platform.orchestration_service
    assert platform.orchestration_service._executor is platform.workflow_executor

    execution = platform.application_facade.analyze(())

    assert execution.is_complete is True
    assert execution.stages[-1] is WorkflowStage.COMPLETED
    assert execution.result["risk_level"] == "low"
    assert service.requests == []
    assert_inactive(platform)


@pytest.mark.parametrize("service", [
    pytest.param(None, id="none"),
    pytest.param(RecordingParsedService(), id="canonical-subclass"),
    pytest.param(FalseyParsedService(), id="falsey-subclass"),
    pytest.param(object(), id="unvalidated-value"),
])
def test_wrapper_forwards_all_inputs_exactly_to_the_root(service, monkeypatch):
    plugins, sources, policy, result = object(), object(), object(), object()
    calls = []

    def build(**kwargs):
        calls.append(kwargs)
        return result

    monkeypatch.setattr(composition.CompositionRoot, "build", staticmethod(build))

    assert composition.build_platform_composition(
        plugins, sources, policy, parsed_document_knowledge_ingestion_service=service,
    ) is result

    assert len(calls) == 1
    assert set(calls[0]) == {
        "plugin_registrations", "capability_availability_sources",
        "mandatory_capability_policy", DEPENDENCY,
    }
    assert calls[0]["plugin_registrations"] is plugins
    assert calls[0]["capability_availability_sources"] is sources
    assert calls[0]["mandatory_capability_policy"] is policy
    assert calls[0][DEPENDENCY] is service
    if isinstance(service, FalseyParsedService):
        assert service.bool_calls == 0
