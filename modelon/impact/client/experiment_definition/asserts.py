from modelon.impact.client import entities


def validate_and_set_initialize_from(entity, definition):
    if isinstance(entity, entities.Experiment):
        if len(entity.get_cases()) > 1:
            raise ValueError(
                "Cannot initialize from an experiment result containing multiple"
                " cases! Please specify a case object instead."
            )
        definition._initialize_from_experiment = entity
    elif isinstance(entity, entities.Case):
        definition._initialize_from_case = entity
    elif isinstance(entity, entities.ExternalResult):
        definition._initialize_from_external_result = entity
    else:
        raise TypeError(
            "The entity argument be an instance of "
            "modelon.impact.client.entities.Case or "
            "modelon.impact.client.entities.Experiment or "
            "modelon.impact.client.entities.ExternalResultUploadOperation!"
        )


def assert_unique_exp_initialization(*initializing_from):
    initializing_from = [entity for entity in initializing_from if entity is not None]
    if len(initializing_from) > 1:
        raise ValueError(
            "An experiment can only be initialized from one entity. Experiment is "
            f"configured to initialize from {' and '.join(map(str, initializing_from))}"
        )