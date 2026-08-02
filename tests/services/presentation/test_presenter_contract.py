from app.services.reasoning.presenter import Presenter
from app.services.reasoning.report_presenter import ReportPresenter


def test_report_presenter_satisfies_presenter_contract() -> None:
    presenter = ReportPresenter()

    assert isinstance(presenter, Presenter)
