# -*- coding: utf-8 -*-
# Description: example netdata python.d module for monitoring Neo4j
# Author: Jerome Baton, copied from Pawel Krupa (paulfantom)


from base import SimpleService
from neo4j.v1 import GraphDatabase




class Service(SimpleService):

    update_every = 30
    priority = 9000
    retries = 1

    def __init__(self, configuration=None, name=None):
        super(self.__class__,self).__init__(configuration=configuration, name=name)
        

    def check(self):
        return True
    
    def create(self):
        self.chart("neo4j.neo4jmonrels", '', 'Monitors the number of nodes per relation name', 'Nodes #','Nodes# per Relation', 'line', self.priority, self.update_every)
        host = self.configuration.get('host')
        boltport = self.configuration.get('boltport','7687')
        uri = "bolt://" + host + ":" + boltport

        self.neodriver = GraphDatabase.driver(uri, auth=(self.configuration.get('user'), self.configuration.get('pwd') ))
        return True

    def update(self, interval):
        self.begin("neo4j.neo4jmonrels", interval)
        neosession = self.neodriver.session()
        
        with neosession.begin_transaction() as tx:
            for neorecord in tx.run("MATCH (n)-[r]-(m) RETURN type(r) as label, count(r) AS cnt ORDER BY cnt DESC LIMIT 5"):
                self.dimension( neorecord["label"] )
                self.set( neorecord["label"], neorecord["cnt"] )
        
        tx.close()        
        neosession.close()

        self.end()
        self.commit()
        
        return True

