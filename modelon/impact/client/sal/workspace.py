"""Workspace service module."""
from typing import Any, Dict, List, Optional

from modelon.impact.client.sal.http import HTTPClient
from modelon.impact.client.sal.uri import URI


class WorkspaceService:
    def __init__(self, uri: URI, http_client: HTTPClient):
        self._base_uri = uri
        self._http_client = http_client

    def workspace_create(self, name: str) -> Dict[str, Any]:
        url = (self._base_uri / "api/workspaces").resolve()
        return self._http_client.post_json(url, body={"new": {"name": name}})

    def workspace_delete(self, workspace_id: str) -> None:
        url = (self._base_uri / f"api/workspaces/{workspace_id}").resolve()
        self._http_client.delete_json(url)

    def workspace_get(self, workspace_id: str, size_info: bool) -> Dict[str, Any]:
        url = (
            self._base_uri / f"api/workspaces/{workspace_id}?sizeInfo={size_info}"
        ).resolve()
        return self._http_client.get_json(url)

    def workspaces_get(
        self,
        only_app_mode: bool = False,
        name: Optional[str] = None,
        sharing_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = {}
        if name:
            query["name"] = name
        if sharing_id:
            query["sharingId"] = sharing_id
        if only_app_mode:
            query["onlyAppMode"] = str(only_app_mode)
        query_args = '&'.join(f'{key}={value}' for key, value in query.items())
        url = (self._base_uri / f"api/workspaces?{query_args}").resolve()
        return self._http_client.get_json(url)

    def projects_get(
        self, workspace_id: str, vcs_info: bool, include_disabled: bool
    ) -> Dict[str, Any]:
        url = (
            self._base_uri
            / f"api/workspaces/{workspace_id}/projects?vcsInfo={vcs_info}"
            f"&includeDisabled={include_disabled}"
        ).resolve()
        return self._http_client.get_json(url)

    def project_create(self, workspace_id: str, name: str) -> Dict[str, Any]:
        url = (self._base_uri / f"api/workspaces/{workspace_id}/projects").resolve()
        return self._http_client.post_json(url, body={"new": {"name": name}})

    def dependencies_get(
        self, workspace_id: str, vcs_info: bool, include_disabled: bool
    ) -> Dict[str, Any]:
        url = (
            self._base_uri
            / f"api/workspaces/{workspace_id}/dependencies?vcsInfo={vcs_info}"
            f"&includeDisabled={include_disabled}"
        ).resolve()
        return self._http_client.get_json(url)

    def workspace_export_setup(
        self, workspace_id: str, publish: bool, class_path: Optional[str] = None
    ) -> Dict[str, Any]:
        url = (self._base_uri / "api/workspace-exports").resolve()
        body = {"workspaceId": workspace_id, 'publish': publish}
        if class_path:
            body['appMode'] = {'model': class_path}
        return self._http_client.post_json(url, body=body)

    def workspace_conversion_setup(
        self, workspace_id: str, backup_name: Optional[str]
    ) -> Dict[str, Any]:
        url = (self._base_uri / "api/workspace-conversions").resolve()
        backup_data = {'backup': {'name': backup_name}} if backup_name else {}
        body: Dict[str, Any] = {'data': {'workspaceId': workspace_id, **backup_data}}
        return self._http_client.post_json(url, body=body)

    def get_workspace_conversion_status(self, location: str) -> Dict[str, Any]:
        url = (self._base_uri / location).resolve()
        return self._http_client.get_json(url)

    def fmus_get(self, workspace_id: str) -> Dict[str, Any]:
        url = (
            self._base_uri / f"api/workspaces/{workspace_id}/model-executables"
        ).resolve()
        return self._http_client.get_json(url)

    def fmu_get(self, workspace_id: str, fmu_id: str) -> Dict[str, Any]:
        url = (
            self._base_uri / f"api/workspaces/{workspace_id}/model-executables/{fmu_id}"
        ).resolve()
        return self._http_client.get_json(url)

    def fmu_download(self, workspace_id: str, fmu_id: str) -> bytes:
        url = (
            self._base_uri
            / f"api/workspaces/{workspace_id}/model-executables/{fmu_id}/binary"
        ).resolve()
        return self._http_client.get_zip(url)

    def experiments_get(
        self, workspace_id: str, class_path: Optional[str] = None
    ) -> Dict[str, Any]:
        class_path_query = f"?classPath={class_path}" if class_path else ""
        url = (
            self._base_uri
            / f"api/workspaces/{workspace_id}/experiments{class_path_query}"
        ).resolve()
        return self._http_client.get_json(
            url, headers={"Accept": "application/vnd.impact.experiment.v2+json"}
        )

    def experiment_get(self, workspace_id: str, experiment_id: str) -> Dict[str, Any]:
        url = (
            self._base_uri
            / f"api/workspaces/{workspace_id}/experiments/{experiment_id}"
        ).resolve()
        return self._http_client.get_json(
            url, headers={"Accept": "application/vnd.impact.experiment.v2+json"}
        )

    def experiment_create(
        self,
        workspace_id: str,
        definition: Dict[str, Any],
        user_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = (self._base_uri / f"api/workspaces/{workspace_id}/experiments").resolve()
        body = {
            **definition,
            **({"userData": user_data} if user_data is not None else {}),
        }
        return self._http_client.post_json(url, body=body)

    def shared_definition_get(
        self, workspace_id: str, strict: bool = False
    ) -> Dict[str, Any]:
        url = (
            self._base_uri / f"api/workspaces/{workspace_id}/"
            f"sharing-definition?strict={'true' if strict else 'false'}"
        ).resolve()
        return self._http_client.get_json(url)

    def import_from_zip(self, path_to_workspace: str) -> Dict[str, Any]:
        url = (self._base_uri / "api/workspace-imports").resolve()
        with open(path_to_workspace, "rb") as f:
            return self._http_client.post_json(url, files={"file": f})

    def import_from_shared_definition(
        self,
        shared_definition: Dict[str, Any],
        selected_matchings: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        if selected_matchings:
            shared_definition = {
                **shared_definition,
                **{"selectedMatchings": {"entries": selected_matchings}},
            }
        url = (self._base_uri / "api/workspace-imports").resolve()
        return self._http_client.post_json(url, body=shared_definition)

    def import_from_cloud(
        self, sharing_id: str, overwrite_workspace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        url = (self._base_uri / "api/workspace-imports").resolve()
        payload: Dict[str, Any] = {"id": sharing_id}
        if overwrite_workspace_id:
            payload["update"] = {"workspaceId": overwrite_workspace_id}
        return self._http_client.post_json(
            url,
            headers={
                "Content-type": "application/vnd.impact.published-workspace.v1+json"
            },
            body=payload,
        )

    def get_project_matchings(
        self, shared_definition: Dict[str, Any]
    ) -> Dict[str, Any]:
        url = (self._base_uri / "api/workspace-imports-matchings").resolve()
        return self._http_client.post_json(url, body=shared_definition)

    def import_project_from_zip(
        self, workspace_id: str, path_to_project: str
    ) -> Dict[str, Any]:
        url = (
            self._base_uri / f"api/workspaces/{workspace_id}/project-imports"
        ).resolve()
        with open(path_to_project, "rb") as f:
            return self._http_client.post_json(url, files={"file": f})

    def import_dependency_from_zip(
        self, workspace_id: str, path_to_project: str
    ) -> Dict[str, Any]:
        url = (
            self._base_uri / f"api/workspaces/{workspace_id}/dependency-imports"
        ).resolve()
        with open(path_to_project, "rb") as f:
            return self._http_client.post_json(url, files={"file": f})

    def get_published_workspaces(
        self,
        name: str = "",
        first: int = 0,
        maximum: int = 20,
        has_data: bool = False,
        owner_username: str = "",
        type: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = {}
        if name:
            query["workspaceName"] = name
        if has_data:
            query["hasData"] = str(has_data)
        if first > 0:
            query["first"] = str(first)
        if maximum >= 0:
            query["max"] = str(maximum)
        if owner_username:
            query["ownerUsername"] = owner_username
        if type:
            query["type"] = type
        query_args = '&'.join(f'{key}={value}' for key, value in query.items())
        url = (self._base_uri / f"api/published-workspaces?{query_args}").resolve()
        resp = self._http_client.get_json_response(url)
        return resp.data

    def get_published_workspaces_by_kind(
        self,
        kind: str = "",
        first: int = 0,
        maximum: int = 20,
    ) -> Dict[str, Any]:
        query = {}
        if kind:
            query["kind"] = kind
        if first > 0:
            query["first"] = str(first)
        if maximum >= 0:
            query["max"] = str(maximum)
        query_args = '&'.join(f'{key}={value}' for key, value in query.items())
        url = (
            self._base_uri / f"/api/published-workspaces/access/users?{query_args}"
        ).resolve()
        resp = self._http_client.get_json_response(url)
        return resp.data

    def get_published_workspace(self, sharing_id: str) -> Dict[str, Any]:
        url = (self._base_uri / f"api/published-workspaces/{sharing_id}").resolve()
        resp = self._http_client.get_json_response(url)
        return resp.data

    def get_published_workspace_acl(self, sharing_id: str) -> Dict[str, Any]:
        url = (
            self._base_uri / f"api/published-workspaces/{sharing_id}/access"
        ).resolve()
        resp = self._http_client.get_json_response(url)
        return resp.data

    def rename_published_workspace(self, sharing_id: str, workspace_name: str) -> None:
        url = (self._base_uri / f"api/published-workspaces/{sharing_id}").resolve()
        self._http_client.patch_json_no_response_body(
            url, body={'workspaceName': workspace_name}
        )

    def _access_request(
        self, operation: str, sharing_id: str, username: Optional[str] = None
    ) -> None:
        url = (
            self._base_uri / f"api/published-workspaces/{sharing_id}/access/users"
        ).resolve()
        body = {"operation": operation}
        if username:
            body['requesterUsername'] = username
        self._http_client.patch_json_no_response_body(url, body=body)

    def _community_access_request(
        self, operation: str, sharing_id: str, username: Optional[str] = None
    ) -> None:
        url = (
            self._base_uri / f"api/published-workspaces/{sharing_id}/access/community"
        ).resolve()
        body = {"operation": operation}
        self._http_client.patch_json_no_response_body(url, body=body)

    def request_published_workspace_access(self, sharing_id: str) -> None:
        self._access_request('request', sharing_id)

    def grant_published_workspace_access(self, sharing_id: str, username: str) -> None:
        self._access_request('grant', sharing_id, username)

    def grant_community_access(self, sharing_id: str) -> None:
        self._community_access_request('grant', sharing_id)

    def revoke_community_access(self, sharing_id: str) -> None:
        self._community_access_request('revoke', sharing_id)

    def revoke_published_workspace_access(self, sharing_id: str, username: str) -> None:
        self._access_request('revoke', sharing_id, username)

    def delete_published_workspace(self, sharing_id: str) -> None:
        url = (self._base_uri / f"api/published-workspaces/{sharing_id}").resolve()
        self._http_client.delete_json(url)

    def update_workspace(
        self, workspace_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        url = (self._base_uri / f"api/workspaces/{workspace_id}").resolve()
        return self._http_client.put_json(url, body=data)
