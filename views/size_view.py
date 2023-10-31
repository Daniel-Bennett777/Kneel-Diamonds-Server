import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create

class SizesView():
    
    def get(self, handler, pk):
        if pk != 0:
            sql = """
            SELECT
                s.id,
                s.carets,
                s.price
            FROM Sizes s
            WHERE s.id = ?
            """
            query_results = db_get_single(sql, pk)
            serialized_size = json.dumps(dict(query_results))

            return handler.response(serialized_size, status.HTTP_200_SUCCESS.value)
        else:
            query_results = db_get_all("SELECT s.id, s.carets, s.price FROM Sizes s")
            sizes = [dict(row) for row in query_results]
            serialized_sizes = json.dumps(sizes)

            return handler.response(serialized_sizes, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Sizes WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, size_data, pk):
        sql = """
        UPDATE Sizes
        SET
            carets = ?,
            price = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (size_data['carets'], size_data['price'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def insert(self, handler, size_data):
        sql = """
        INSERT INTO Sizes (carets, price) VALUES (?, ?)
        """
        new_item = db_create(sql, (size_data['carets'], size_data['price']))

        if new_item is not None:
            # Build a response dictionary with the created resource's ID
            response_data = {
                "id": new_item,
                "carets": size_data['carets'],
                "price": size_data['price']
            }

            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)