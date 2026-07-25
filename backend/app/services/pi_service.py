from app.models.pi_tag import PITag


class PIService:
    def __init__(self):
        self.tags = {}

    def update_tag(self, tag: PITag):
        self.tags[tag.tag_name] = tag

    def get_tag(self, tag_name: str):
        return self.tags.get(tag_name)

    def get_all_tags(self):
        return list(self.tags.values())
