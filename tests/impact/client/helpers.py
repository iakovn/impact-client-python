from modelon.impact.client.entities.custom_function import CustomFunction
from modelon.impact.client.entities.workspace import Workspace, WorkspaceDefinition
from modelon.impact.client.entities.experiment import Experiment
from modelon.impact.client.entities.model_executable import ModelExecutable
from modelon.impact.client.entities.case import Case
from modelon.impact.client.entities.project import (
    Project,
    ProjectContent,
    ProjectDefinition,
    ProjectType,
    VcsUri,
)
from modelon.impact.client.entities.external_result import ExternalResult
from modelon.impact.client.entities.model import Model
from modelon.impact.client.operations.experiment import ExperimentOperation
from modelon.impact.client.operations.model_executable import (
    CachedModelExecutableOperation,
    ModelExecutableOperation,
)
from unittest.mock import MagicMock


class IDs:
    WORKSPACE_PRIMARY = 'workspace_1'
    WORKSPACE_SECONDARY = 'workspace_2'
    PROJECT_PRIMARY = 'bf1e2f2a2fd55dcfd844bc1f252528f707254425'
    PROJECT_SECONDARY = 'xbhcdhcbdbchdbhcbdhbchdchdhcbhdbchdbch'
    PROJECT_CONTENT_PRIMARY = '81ac23172d7a479db85126691e090b34'
    PROJECT_CONTENT_SECONDARY = 'f727f04210b94a0fac81f17f83b869e6'
    VERSIONED_PROJECT_REFERENCE = '4019c58d4a3b41fc463934274ece3f9a0ac27436'
    VERSIONED_PROJECT_PRIMARY = 'c1f1d74f0b612c6b67e4165bf9a1ad30b2630039'
    VERSIONED_PROJECT_SECONDARY = 'da282cc77feaa60fc93879a7f39e27ab78304940'
    MSL_400_PROJECT_ID = 'cdbde8922bd2c48c392b1b4bb740adc0273c737c'
    MSL_300_PROJECT_ID = '84fb1c37abe6ed97a53972fb7239630e1212438b'
    MSL_CONTENT_ID = '925cbe6daaf3ebde61dfcc2a26f93e6d0798085a'
    FMU_PRIMARY = 'test_pid_fmu_id'
    FMU_SECONDARY = 'test_filter_fmu_id'
    EXPERIMENT_PRIMARY = 'pid_20090615_134'
    EXPERIMENT_SECONDARY = 'filter_20090615_135'
    IMPORT = '9a8fg798a7g'


VERSIONED_PROJECT_TRUNK = {
    "id": IDs.VERSIONED_PROJECT_PRIMARY,
    "definition": {
        "name": "NewProjectTrunk",
        "format": "1.0",
        "content": [
            {
                "id": IDs.PROJECT_CONTENT_PRIMARY,
                "relpath": "MyPackage",
                "contentType": "MODELICA",
                "name": "MyPackage",
                "defaultDisabled": False,
            }
        ],
    },
    "projectType": "LOCAL",
    "vcsUri": {
        "serviceKind": "git",
        "serviceUrl": "https://github.com",
        "repoUrl": {
            "url": "github.com/project/test.git",
            "refname": "master",
            "sha1": "cd8fe4f6e2bff02f88fc1baeb7260c83160ee927",
        },
        "protocol": "https",
        "subdir": ".",
    },
}
VERSIONED_PROJECT_BRANCH = {
    "id": IDs.VERSIONED_PROJECT_SECONDARY,
    "definition": {
        "name": "NewProjectBranch",
        "format": "1.0",
        "content": [
            {
                "id": IDs.PROJECT_CONTENT_SECONDARY,
                "relpath": "MyPackage",
                "contentType": "MODELICA",
                "name": "MyPackage",
                "defaultDisabled": False,
            }
        ],
    },
    "projectType": "LOCAL",
    "vcsUri": {
        "serviceKind": "git",
        "serviceUrl": "https://github.com",
        "repoUrl": {
            "url": "github.com/project/test.git",
            "refname": "master",
            "sha1": "incndcj6e2bff02f88fc1baeb7260c83160ee927",
        },
        "protocol": "https",
        "subdir": ".",
    },
}


def get_test_workspace_definition(name=None):
    return {
        "name": name if name else IDs.WORKSPACE_PRIMARY,
        "format": "1.0",
        "description": "",
        "createdBy": "local-installation-user-id",
        "createdAt": "1659072911361",
        "defaultProjectId": IDs.PROJECT_PRIMARY,
        "projects": [
            {
                "reference": {"id": IDs.PROJECT_PRIMARY},
                "disabled": False,
                "disabledContent": [],
            },
            {
                "reference": {
                    "id": IDs.VERSIONED_PROJECT_REFERENCE,
                    "vcsUri": "git+https://github.com/project/test.git@main:da6abb188a089527df1b54b27ace84274b819e4a",
                },
                "disabled": True,
                "disabledContent": [],
            },
        ],
        "dependencies": [
            {
                "reference": {
                    "id": IDs.MSL_300_PROJECT_ID,
                    "name": "MSL",
                    "version": "3.2.3",
                },
                "disabled": True,
                "disabledContent": [],
            },
            {
                "reference": {
                    "id": IDs.MSL_400_PROJECT_ID,
                    "name": "MSL",
                    "version": "4.0.0",
                },
                "disabled": False,
                "disabledContent": [],
            },
        ],
    }


def create_workspace_entity(name, definition=None, service=None):
    if not definition:
        definition = get_test_workspace_definition(name)
    return Workspace(name, WorkspaceDefinition(definition), service or MagicMock())


def create_model_entity(
    class_name, workspace_id, project_id, service=None,
):
    return Model(class_name, workspace_id, project_id, service or MagicMock())


def create_model_exe_entity(
    workspace_id, fmu_id, service=None, info=None, modifiers=None,
):
    return ModelExecutable(
        workspace_id, fmu_id, service or MagicMock(), info, modifiers,
    )


def create_experiment_entity(
    workspace_id, exp_id, service=None, info=None,
):
    return Experiment(workspace_id, exp_id, service or MagicMock(), info)


def create_project_entity(
    project_id,
    project_name="my_project",
    definition=None,
    project_type=ProjectType.LOCAL,
    vcs_uri=None,
    service=None,
):
    if not definition:
        definition = {
            "name": project_name,
            "format": "1.0",
            "dependencies": [{"name": "MSL", "versionSpecifier": "4.0.0"}],
            "content": [
                {
                    "id": IDs.PROJECT_CONTENT_PRIMARY,
                    "relpath": "MyPackage",
                    "contentType": "MODELICA",
                    "name": "MyPackage",
                    "defaultDisabled": False,
                }
            ],
            "executionOptions": [],
        }
    return Project(
        project_id,
        ProjectDefinition(definition),
        project_type,
        VcsUri.from_dict(vcs_uri) if vcs_uri else None,
        service or MagicMock(),
    )


def create_project_content_entity(
    project_id, content_id=IDs.PROJECT_CONTENT_PRIMARY, content=None, service=None,
):
    if not content:
        content = {
            "id": content_id,
            "relpath": "MyPackage",
            "contentType": "MODELICA",
            "name": "MyPackage",
            "defaultDisabled": False,
        }
    return ProjectContent(content, project_id, service or MagicMock())


def create_case_entity(
    case_id, workspace_id, exp_id, service=None, info=None,
):
    return Case(case_id, workspace_id, exp_id, service or MagicMock(), info)


def create_external_result_entity(result_id, service=None):
    return ExternalResult(result_id, service or MagicMock())


def create_custom_function_entity(
    workspace_id, name, parameter_data=None, service=None
):
    return CustomFunction(
        workspace_id, name, parameter_data or [], service or MagicMock()
    )


def create_experiment_operation(
    workspace_id, exp_id, service=None,
):
    return ExperimentOperation(workspace_id, exp_id, service or MagicMock())


def create_cached_model_exe_operation(
    workspace_id, fmu_id, service=None, info=None, modifiers=None,
):
    return CachedModelExecutableOperation(
        workspace_id, fmu_id, service or MagicMock(), info=info, modifiers=modifiers,
    )


def create_model_exe_operation(
    workspace_id, fmu_id, service=None,
):
    return ModelExecutableOperation(workspace_id, fmu_id, service or MagicMock())
