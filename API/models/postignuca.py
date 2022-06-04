import psycopg2
from db import *

def get_postignuce_by_id_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur= conn.cursor()
    cur.execute("select * from sbp.postignuca as ps where ps.id ="+ str(id)+";")
    postignuce=cur.fetchone()
    cur.execute("select ko.id , ko.komentar_sadrzaj, ko.created_at, ko.korisnik_id from sbp.komentari as ko where ko.postignuce_id ="+ str(id)+";")
    kom=cur.fetchall()
    cur.execute("select s.id , s.link_slike, s.naziv, s.opis from sbp.slike_postignuca as s where s.postignuce_id="+ str(id)+";")
    sl=cur.fetchall()
    response= {"id":postignuce[0], "korisnik_id":postignuce[1], "naslov":postignuce[2], "opis":postignuce[3], "link_gpx_traga":postignuce[4], "created_at":str(postignuce[5]), "updated_at":str(postignuce[6]), "komentari":[], "slike":[]}
    for row in kom:
        x={"id":row[0], "komentar":row[1], "created_at":str(row[2]), "korisnik_id":row[3]}
        response["komentari"].append(x)
    
    for row in sl:
        x={"id":row[0], "link_slike":row[1], "naziv":row[2], "opis":row[3]}
        response["slike"].append(x)
    
    return response

def post_postignuce_pg(korisnik_id, naslov, opis, link):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur = conn.cursor()
    cur.execute("INSERT INTO sbp.postignuca (korisnik_id, naslov, opis, link_gpx_traga) VALUES ('{}','{}','{}','{}');".format(korisnik_id, naslov, opis, link))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}