from api.arthub_api import get_child_node_id_in_range, get_node_brief_by_id


class ArtHub(object):

    def __init__(self, token, domain, depot):
        self.header = {"publictoken": token}
        self.domain = domain
        self.depot = depot

    @staticmethod
    def get_resp_result(resp: dict):
        code = resp.get("code")
        if code is None or code != 0:
            return None

        return resp.get("result")

    def get_asset_folder_by_path(self, path: list, folder_id):
        if len(path) == 0:
            return folder_id

        node_name = path[0]
        child_nodes_resp = get_child_node_id_in_range(f"{self.domain}/{self.depot}/data/openapi/v2/core/get-child-node-id-in-range", folder_id, self.header)
        child_nodes_result = self.get_resp_result(child_nodes_resp)
        if not child_nodes_result:
            return None

        nodes = child_nodes_result.get("nodes")
        nodes_detail_resp = get_node_brief_by_id(f"{self.domain}/{self.depot}/data/openapi/v2/core/get-node-brief-by-id", nodes, self.header)
        nodes_detail_result = self.get_resp_result(nodes_detail_resp)
        if not nodes_detail_result:
            return None

        for x in nodes_detail_result.get("items"):
            if x.get("name") == node_name:
                return self.get_asset_folder_by_path(path[1:], x.get("id"))

        return None


if __name__ == '__main__':
    arthub = ArtHub("2012b", "http://arthub-api.h3d.com.cn", "h3d")
    res = arthub.get_asset_folder_by_path(["tag_upload_test", "原画", "X51", "PSD库", "2021年", "2021年09月版本", "商业化"], 100002)
    print(res)
