ORACLE_COLUMNS_TO_ENDECA = {'FULFILLMENT_DATE':'mdex:dateTime', 'GL_DATE' : 'mdex:dateTime',
				'SHIP_QUANTITY': 'mdex:int', 'UNIT_PRICE':'mdex:double', 'ORDERED_QUANTITY':'mdex:int',
				 'PROMISE_DATE': 'mdex:dateTime', 'SCHEDULE_SHIP_DATE' :'mdex:dateTime', 'REQUEST_DATE':'mdex:dateTime',
				 'SHIPPED_QUANTITY' : 'mdex:int', 'ACTUAL_SHIPMENT_DATE':'mdex:dateTime',
				 'ACTUAL_ARRIVAL_DATE' : 'mdex:dateTime', 'ULTIMATE_DROPOFF_DATE': 'mdex:dateTime'}

ENDECA_TO_XML = {'mdex:double': 'number', 'mdex:string': 'string', 'mdex:boolean': 'boolean',
                            'mdex:dateTime': 'date', 'mdex:int': 'integer',
                            'mdex:long': 'long'}