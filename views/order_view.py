import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create

class OrderView():

    def get_expanded(self, handler, pk, expand_params):
        # Initial SQL query for the Orders table
        sql = "SELECT * FROM Orders WHERE id = ?"
        order = db_get_single(sql, pk)
        
        if not order:
            return handler.response("Order not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        # Check for expansions
        expanded_data = {}
        if "metals" in expand_params:
            # Retrieve metal data
            metal_sql = "SELECT id, metal, price FROM Metals WHERE id = ?"
            metal_data = db_get_single(metal_sql, order["id"])

            if metal_data:
                expanded_data["metal"] = {
                    "id": order["metalId"],
                    "metal": metal_data["metal"],
                    "price": metal_data["price"]
                }

        if "sizes" in expand_params:
            # Add sizes expansion
            size_sql = "SELECT id, carets, price FROM Sizes WHERE id = ?"
            size_data = db_get_single(size_sql, order["sizeId"])
            if size_data:
                expanded_data["size"] = {
                    "id": order["sizeId"],
                    "carets": size_data["carets"],
                    "price": size_data["price"]
                }

        if "styles" in expand_params:
            # Add styles expansion
            style_sql = "SELECT id, style, price FROM Styles WHERE id = ?"
            style_data = db_get_single(style_sql, order["styleId"])
            if style_data:
                expanded_data["style"] = {
                    "id": order["styleId"],
                    "style": style_data["style"],
                    "price": style_data["price"]
                }
        # Add the order data to the response
        response_data = [dict(order)]
        response_data[0].update(expanded_data)
        return handler.response(json.dumps(response_data), status.HTTP_200_SUCCESS.value)

    def get(self, handler, pk):
        if pk != 0:
            order = db_get_single("SELECT * FROM Orders WHERE id = ?", pk)
            if order:
                return handler.response(json.dumps(dict(order)), status.HTTP_200_SUCCESS.value)
            return handler.response("Order not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        else:
            orders = db_get_all("SELECT * FROM Orders")
            if orders:
                serialized_orders = [dict(order) for order in orders]
                return handler.response(json.dumps(serialized_orders), status.HTTP_200_SUCCESS.value)
            return handler.response("No orders found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Orders WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("Order not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, order_data, pk):
        sql = """
        UPDATE Orders
        SET
            metalId = ?,
            sizeId = ?,
            styleId = ?,
            timestamp = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (order_data['metalId'], order_data['sizeId'], order_data['styleId'], order_data['timestamp'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("Order not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def insert(self, handler, order_data):
        sql = """
        INSERT INTO Orders (metalId, sizeId, styleId, timestamp) VALUES (?, ?, ?, ?)
        """

        new_item = db_create(sql, (order_data['metalId'], order_data['sizeId'], order_data['styleId'], order_data['timestamp']))

        if new_item is not None:
            response_data = {
                "id": new_item,
                "metalId": order_data['metalId'],
                "sizeId": order_data['sizeId'],
                "styleId": order_data['styleId'],
                "timestamp": order_data['timestamp']
            }

            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("Error", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)