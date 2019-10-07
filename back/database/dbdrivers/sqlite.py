import sqlite3 as sql
import json

class sqlite:

   instancia = None

   def __new__(cls, conf, *args, **kargs):
      if cls.instancia is None:
         cls.instancia = object.__new__(cls, *args, **kargs)
         cls.instancia.db=conf['DATABASE']['DB']
      return cls.instancia


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
         for value in where:
            if cont==1 and len(where)==1:
               query3+="("+str("'"+value+"'")+")"
            elif cont==1 and len(where)>1:
               query3+= "("+ str("'"+value+"'")+", "
            elif cont==len(where):
               query3+= str("'"+value+"'")+")"
            else:
               query3+= str("'"+value+"'")+", "
            cont+=1
         query+=query3
      return query


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
      return query2

   def query(self, query, where=None, where2=None,  resType="array"):
      try:
         self.conexion = sql.connect(self.db)
         self.cursor= self.conexion.cursor()
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
               comprobacion="select count(*) from sqlite_master where type='table' and name="+"'"+nombreTabla + "'"
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
      except sql.Error as err:
         res=False
      return res