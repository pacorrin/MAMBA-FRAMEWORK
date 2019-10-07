import mysql.connector as mc
import json
from mysql.connector import errorcode

#Singleton
class mysql:
   instancia = None

   # def __new__(cls, conf, *args, **kargs):
   #    if cls.instancia is None:
   #       cls.instancia = object.__new__(cls, *args, **kargs)
   #       cls.instancia.host=conf['DATABASE']['HOST']
   #       cls.instancia.db=conf['DATABASE']['DB']
   #       cls.instancia.usr=conf['DATABASE']['USER']
   #       cls.instancia.passwd=conf['DATABASE']['PASSWORD']
   #       cls.instancia.port=conf['DATABASE']['PORT']
   #    return cls.instancia

   def __init__(self,conf):
      self.host=conf['DATABASE']['HOST']
      self.db=conf['DATABASE']['DB']
      self.usr=conf['DATABASE']['USER']
      self.passwd=conf['DATABASE']['PASSWORD']
      self.port=conf['DATABASE']['PORT']

   def toJson(self, cursor, desCursor):
      rows = [x for x in cursor]
      cols = [x[0] for x in desCursor]
      elems = []
      for row in rows:
         elem = {}
         for prop, val in zip(cols, row):
            elem[prop] = val
         elems.append(elem)   
      return elems

   
   def select (self, query, where):
      if where != None:
            query2=""
            values = where.items()
            cont=0
            for key,value in values:               
               if cont == 0:
                  query2+= " WHERE "+ str(key) +  str("'"+value+"'")
               else:
                  query2+= " AND "+ str(key) + str("'"+value+"'")
               cont+=1
            query+=query2   

      print(query)
      return query

   def insert (self, query, where):
      query2=""
      query3=" VALUES"
      cont=1
      if isinstance(where, dict):
         elems=where.items()
         for key,value in elems:
            if cont==1 and len(where)==1:
               query2+= "("+str(key) +")"
               query3+= "("+str("'"+value+"'")+")"
            elif cont==1 and len(where)>1:
               query2+= "("+str(key) +", "
               query3+= "("+ str("'"+value+"'")+", "
            elif cont==len(where):
               query2+= str(key) +")"
               query3+= str("'"+value+"'")+")"
            else:
               query2+= str(key) +", "
               query3+= str("'"+value+"'")+", "
            cont+=1
         query+=(query2+query3)
      if isinstance(where, list):
         valuesStr = " VALUES ("
         for value in where:
            if value == "NULL" or value == "NOW()" or type(value) is int:
               valuesStr += value.__str__() + ","
            else: 
               valuesStr += "'" + value.__str__() + "',"

         valuesStr = valuesStr.rstrip(",") + ")"
      print(query + valuesStr)
      return query + valuesStr


   def update(self,query,where,where2):
      query2=" SET "
      query3= " WHERE "
      cont=1
      cont2=1
      elems=where.items()
      elems2=where2.items()
      for key,value in elems:
         if cont==len(elems):
            query2+=str(key)+"="+str("'"+value+"'")
         else:
            query2+=str(key)+"="+str("'"+value+"'")+", "
         cont+=1
      for key,value in elems2:
         if cont2==1 and len(elems2)==1:
            query3+=str(key)+str("'"+value+"'")
         elif cont2==1 and len(elems2)>1:
            query3+=str(key)+str("'"+value+"'")+" AND "
         elif cont2==len(elems2):
            query3+=str(key)+str("'"+value+"'")
         else:
            query3+=str(key)+str("'"+value+"'")+" AND "
         cont2+=1
      query+=(query2+query3)
      return query

   def delete (self,query,where):
      query2=" WHERE "
      cont=1
      elems=where.items()
      for key,value in elems:
         if cont==len(elems):
            query2+=str(key)+str("'"+value+"'")
         else:
            query2+=str(key)+str("'"+value+"'")+"AND "
         cont+=1
      query+=query2
      return query

   def createTable(self,query,where):
      query2=query +" ("
      cont=1
      elems=where.items()
      for key,value in elems:
         if cont==1 and len(elems)==1 or cont==len(elems) :
            query2+=str(key)+" "+str(value[0])+" "+str(value[1])+")"
         elif cont==1 and len(elems)>1:
            query2+=str(key)+" "+str(value[0])+" "+str(value[1])+ " PRIMARY KEY"+", "
         else:
            query2+=str(key)+" "+str(value[0])+" "+str(value[1])+", "
         cont+=1
      print(query2)
      return query2


   def query(self, query, where=None, where2=None,  resType="array"):
      try:
         self.conexion=mc.connect( host=self.host, database=self.db,
         user=self.usr, passwd=self.passwd, port=self.port)
      except mc.Error as err:
         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('No se puede acceder a la BD.')
         elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('No existe la base de datos')
         else:
            print('Fallo en la conexión a la BD')
      try:
         self.cursor=self.conexion.cursor()
         if "select" in query or "Select" in query or "SELECT" in query:   
            self.cursor.execute(self.select(query,where))
            if(resType=="array"):
               res=self.cursor.fetchall()
            elif(resType=="json" or resType=="JSON"):
               yeison=self.toJson(self.cursor, self.cursor.description)
               res=json.dumps(yeison)

         if "insert" in query or "Insert" in query or "INSERT" in query:
            if where !=None:
               self.cursor.execute(self.insert(query,where))
               if(self.cursor.rowcount >= 1):
                  res=True
               else:
                  res=False
            else:
               res=False
            self.conexion.commit()
            
         if "update" in query or "Update" in query or "UPDATE" in query:
            if where !=None and where2 != None:
               self.cursor.execute(self.update(query,where,where2))
               if(self.cursor.rowcount >= 1):
                  res=True
               else:
                  res=False
            else:
               res=False
            self.conexion.commit()

         if "delete" in query or "Delete" in query or "DELETE" in query:
            if where !=None:
               self.cursor.execute(self.delete(query,where))
               if(self.cursor.rowcount >= 1):
                  res=True
               else:
                  res=False
            else:
               res=False
            self.conexion.commit()

         if "create" in query or "CREATE" in query and "table" in query or "TABLE" in query:
            if where !=None:
               word_list = query.split() 
               nombreTabla= word_list[-1]
               comprobacion="select count(*) from information_schema.TABLES WHERE (TABLE_SCHEMA =" + "'"+ self.db + "'"+ ") AND (TABLE_NAME =" + "'" + nombreTabla + "'"+")"
               self.cursor.execute(comprobacion)
               if(str(self.cursor.fetchall())=="[(1,)]"):
                  print("Ya existe")
                  res=False
               else:
                  self.cursor.execute(self.createTable(query,where))
                  res=True
            else:
               res=False
            self.conexion.commit()

         self.cursor.close()
         self.conexion.close()
      except mc.Error as err:
         res=False
         print(err)
      return res