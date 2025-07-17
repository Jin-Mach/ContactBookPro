from src.database.models.mandatory_model import MandatoryModel


class SearchProvider:

    @staticmethod
    def basic_search(mandatory_model: MandatoryModel, new_filter: str) -> None:
        mandatory_model.setFilter(new_filter)

    @staticmethod
    def reset_filter(mandatory_model: MandatoryModel) -> None:
        mandatory_model.setFilter("")