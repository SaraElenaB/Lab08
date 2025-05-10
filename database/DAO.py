from database.DB_connect import DBConnect
from model.nerc import Nerc
from model.powerOutages import Event


class DAO():
    def __init__(self):
        pass

    # -----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllNerc():
        cnx = DBConnect.get_connection()
        ris = []

        cursor = cnx.cursor(dictionary=True)
        query = """ select * from Nerc n """

        cursor.execute(query)

        #lista di ogg Nerc
        for row in cursor:
            ris.append( Nerc( row["id"],
                              row["value"]))
        cursor.close()
        cnx.close()
        return ris

    # -----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEvents(nerc):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * 
                    from eventtype e, poweroutages p
                    where e.id = p.event_type_id
                    and p.nerc_id = %s"""

        cursor.execute(query, (nerc.id,))


        for row in cursor:
            result.append(
                Event(row["id"], row["event_type_id"],
                      row["tag_id"], row["area_id"],
                      row["nerc_id"], row["responsible_id"],
                      row["customers_affected"], row["date_event_began"],
                      row["date_event_finished"], row["demand_loss"]))

        cursor.close()
        conn.close()
        return result

    # -----------------------------------------------------------------------------------------------------------------------------