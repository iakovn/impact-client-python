from pathlib import Path

from modelon.impact.client import ContentType
from modelon.impact.client.operations.base import AsyncOperationStatus
from tests.files.paths import SINGLE_FILE_LIBRARY_PATH
from tests.impact.client.helpers import (
    IDs,
    create_project_content_entity,
    create_project_entity,
)


class TestProject:
    def test_get_project_size(self, project):
        assert project.entity.size == 1008

    def test_get_project_options(self, project, custom_function):
        options = project.entity.get_options(custom_function)
        assert options.to_dict() == {
            "compiler": {
                "c_compiler": "gcc",
                "generate_html_diagnostics": False,
                "include_protected_variables": False,
            },
            "runtime": {"log_level": 2},
            "simulation": {'dynamic_diagnostics': False, 'ncp': 500},
            "solver": {"rtol": 1e-5},
            'customFunction': IDs.DYNAMIC_CF,
        }

    def test_get_project_default_options(self, project, custom_function):
        options = project.entity.get_options(custom_function, use_defaults=True)
        assert options.to_dict() == {
            'compiler': {'c_compiler': 'gcc'},
            'customFunction': IDs.DYNAMIC_CF,
        }

    def test_get_project_contents(self, project):
        contents = project.entity.get_contents()
        assert len(contents) == 1
        assert contents[0].id == IDs.PROJECT_CONTENT_PRIMARY
        assert contents[0].relpath == Path('MyPackage')
        assert contents[0].content_type == ContentType.MODELICA
        assert contents[0].name == 'MyPackage'
        assert not contents[0].default_disabled

    def test_get_project_content_by_id(self, project):
        content = project.entity.get_content(IDs.PROJECT_CONTENT_SECONDARY)
        assert content.id == IDs.PROJECT_CONTENT_SECONDARY
        assert content.relpath == Path('test.mo')
        assert content.content_type == ContentType.MODELICA
        assert content.name == 'test'
        assert not content.default_disabled

    def test_get_project_content_by_name(self, project):
        content = project.entity.get_content_by_name('MyPackage', ContentType.MODELICA)
        assert content.id == IDs.PROJECT_CONTENT_PRIMARY
        assert content.relpath == Path('MyPackage')
        assert content.content_type == ContentType.MODELICA
        assert content.name == 'MyPackage'
        assert not content.default_disabled

    def test_get_modelica_library_by_name(self, project):
        content = project.entity.get_modelica_library_by_name('MyPackage')
        assert content.id == IDs.PROJECT_CONTENT_PRIMARY
        assert content.relpath == Path('MyPackage')
        assert content.content_type == ContentType.MODELICA
        assert content.name == 'MyPackage'
        assert not content.default_disabled

    def test_delete_project_contents(self, project):
        service = project.service
        content = create_project_content_entity(
            project_id=IDs.PROJECT_PRIMARY,
            service=project.service,
        )
        content.delete()
        service.project.project_content_delete.assert_called_with(
            IDs.PROJECT_PRIMARY,
            IDs.PROJECT_CONTENT_PRIMARY,
        )

    def test_delete_project(self, project):
        service = project.service
        project = create_project_entity(
            project_id=IDs.PROJECT_PRIMARY,
            service=service,
        )
        project.delete()
        service.project.project_delete.assert_called_with(IDs.PROJECT_PRIMARY)

    def test_import_content(self, project):
        content_operation = project.entity.import_content(
            SINGLE_FILE_LIBRARY_PATH, content_type=ContentType.MODELICA
        )
        assert content_operation.status == AsyncOperationStatus.READY
        content = content_operation.data()

        assert content.id == IDs.PROJECT_CONTENT_SECONDARY
        assert content.relpath == Path('test.mo')
        assert content.content_type == ContentType.MODELICA
        assert content.name == 'test'
        assert not content.default_disabled

    def test_import_modelica_library(self, project):
        content_operation = project.entity.import_modelica_library(
            SINGLE_FILE_LIBRARY_PATH
        )
        assert content_operation.status == AsyncOperationStatus.READY

        content = content_operation.data()
        assert content.id == IDs.PROJECT_CONTENT_SECONDARY
        assert content.relpath == Path('test.mo')
        assert content.content_type == ContentType.MODELICA
        assert content.name == 'test'
        assert not content.default_disabled
