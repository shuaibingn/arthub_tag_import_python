from api.arthub_api import get_child_node_id_in_range, get_node_brief_by_id, get_tag_id_by_asset_id, get_tag_detail_by_id, delete_asset_tag, add_asset_tag

from utils.exception import ArtHubException, api_response_error, not_find_child_node, delete_tag_error, add_tag_error


id_cache = {}


class ArtHub(object):

    def __init__(self, token, domain, depot):
        self.header = {"publictoken": token}
        self.domain = domain
        self.depot = depot

    @staticmethod
    def get_resp_result(resp: dict):
        code = resp.get("code")
        if code is None or code != 0:
            raise ArtHubException(api_response_error.format(code))

        return resp.get("result")

    def add_tag(self, path, folder_id, tag_name, is_recursion=False):
        asset_folder_id = self.get_asset_folder_by_path(path, folder_id, "")
        asset_ids_list = self.get_asset_ids(asset_folder_id, is_recursion)

        for asset_id in asset_ids_list:
            self.delete_tag_by_asset_id(asset_id)
            self.add_asset_tag(asset_id, tag_name)

    def get_child_node_detail_by_folder_id(self, folder_id):
        child_nodes_resp = get_child_node_id_in_range(f"{self.domain}/{self.depot}/data/openapi/v2/core/get-child-node-id-in-range", folder_id, self.header)
        child_nodes_result = self.get_resp_result(child_nodes_resp)

        nodes = child_nodes_result.get("nodes")
        nodes_detail_resp = get_node_brief_by_id(f"{self.domain}/{self.depot}/data/openapi/v2/core/get-node-brief-by-id", nodes, self.header)
        nodes_detail_result = self.get_resp_result(nodes_detail_resp)
        return nodes_detail_result

    def get_asset_folder_by_path(self, path: list, folder_id, folder_name):
        if len(path) == 0:
            return folder_id

        node_name = path[0]
        folder_name += node_name + "."
        cache_id = id_cache.get(folder_name)
        if cache_id is not None:
            return self.get_asset_folder_by_path(path[1:], cache_id, folder_name)

        nodes_detail_result = self.get_child_node_detail_by_folder_id(folder_id)
        for x in nodes_detail_result.get("items"):
            if x.get("name") == node_name:
                id_cache[folder_name] = x.get("id")
                return self.get_asset_folder_by_path(path[1:], x.get("id"), folder_name)

        raise ArtHubException(not_find_child_node)

    def get_asset_ids(self, folder_id, is_recursion=False):
        if is_recursion:
            return self.get_asset_id_by_asset_folder_id_recursion([folder_id], [])

        return self.get_asset_id_by_asset_folder_id(folder_id)

    def get_asset_id_by_asset_folder_id(self, asset_folder_id):
        asset_ids = []

        nodes_detail_result = self.get_child_node_detail_by_folder_id(asset_folder_id)
        if nodes_detail_result:
            for x in nodes_detail_result.get("items"):
                if x.get("node_type") == "asset":
                    asset_ids.append(x.get("id"))

        return asset_ids

    def get_asset_id_by_asset_folder_id_recursion(self, asset_folder_ids: list, asset_ids: list) -> list:
        if len(asset_folder_ids) == 0:
            return asset_ids

        folder_ids = []
        for asset_folder_id in asset_folder_ids:
            nodes_detail_result = self.get_child_node_detail_by_folder_id(asset_folder_id)
            if nodes_detail_result:
                for x in nodes_detail_result.get("items"):
                    if x.get("node_type") == "directory":
                        folder_ids.append(x.get("id"))
                    elif x.get("node_type") == "asset":
                        asset_ids.append(x.get("id"))

        return self.get_asset_id_by_asset_folder_id_recursion(folder_ids, asset_ids)

    def delete_tag_by_asset_id(self, asset_id) -> bool:
        tag_ids_resp = get_tag_id_by_asset_id(f"{self.domain}/{self.depot}/data/openapi/v2/core/get-tag-id-by-asset-id", asset_id, self.header)
        tag_ids = self.get_resp_result(tag_ids_resp)
        if len(tag_ids) == 0:
            return True

        tag_name = []
        tag_detail_resp = get_tag_detail_by_id(f"{self.domain}/{self.depot}/data/openapi/v2/core/get-tag-detail-by-id", tag_ids, self.header)
        tag_detail = self.get_resp_result(tag_detail_resp)
        for x in tag_detail:
            tag_name.append(x.get("tag_name"))

        delete_asset_resp = delete_asset_tag(f"{self.domain}/{self.depot}/data/openapi/v2/core/delete-asset-tag", asset_id, tag_name, self.header)
        code = delete_asset_resp.get("code")
        if code is not None and code != 0:
            raise ArtHubException(delete_tag_error)

        return True

    def add_asset_tag(self, asset_id, tag_name) -> bool:
        add_asset_tag_resp = add_asset_tag(f"{self.domain}/{self.depot}/data/openapi/v2/core/add-asset-tag", asset_id, tag_name, self.header)
        code = add_asset_tag_resp.get("code")
        if code is not None and code != 0:
            raise ArtHubException(add_tag_error)

        return True
