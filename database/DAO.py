from database.DB_connect import DBConnect
from modello.conteggio import Conteggio
from modello.prodotto import Prodotto

class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """SELECT DISTINCT (YEAR (gds.`Date`))
                    FROM go_daily_sales gds """
        cursor.execute(query, ())

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getColore():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = """SELECT DISTINCT gp.Product_color 
                    FROM go_products gp  """
        cursor.execute(query, ())

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getProdotti(colore):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  gp.*
                    FROM go_products gp 
                    WHERE gp.Product_color =%s """
        cursor.execute(query, (colore,))

        for row in cursor:
            result.append(Prodotto(**row))
        #print(result)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getCombinazioneProdotti(anno,colore):
            conn = DBConnect.get_connection()

            result = []

            cursor = conn.cursor(dictionary=True)
            query = """SELECT DISTINCT
    gds1.Product_number AS Product_number1,
    gds2.Product_number AS Product_number2, COUNT(DISTINCT gds2.`Date`) as Conteggio
FROM 
    go_daily_sales gds1
JOIN 
    go_daily_sales gds2 
ON 
    gds1.Retailer_code = gds2.Retailer_code 
    AND gds1.Date = gds2.Date
    AND gds1.Product_number < gds2.Product_number
JOIN 
    go_products gp1
ON 
    gds1.Product_number = gp1.Product_number
JOIN 
    go_products gp2
ON 
    gds2.Product_number = gp2.Product_number
WHERE 
    YEAR(gds1.Date) = %s
    AND YEAR(gds2.Date) = %s
    AND gp2.Product_color =%s
    AND gp1.Product_color=%s
GROUP by
    gds1.Product_number,
    gds2.Product_number 

 """
            cursor.execute(query, (anno,anno,colore, colore))

            for row in cursor:
                result.append(Conteggio(**row))
            #print(result)
            cursor.close()
            conn.close()
            return result



if __name__=="__main__":
    print(DAO.getAnni())
    print(DAO.getColore())
    DAO.getProdotti("Red")
    print(len(DAO.getCombinazioneProdotti(2017,"blue")))