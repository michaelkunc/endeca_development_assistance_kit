import openpyxl


class SQL(object):
	DEFINE_OFF = 'SET DEFINE OFF;\n'
	COMMIT = 'COMMIT;'
	SCHEMA = 'APPS'
	EBS_LANGUAGE_CODES  = ('D', 'DK', 'E', 'F', 'NL', 'PT', 'PTB', 'S', 'US', 'ZHS')
	REM_INSERT = 'REM INSERTING into '
	INSERT_INTO = 'Insert into '
#need to add an attribute source as a parameter

	def __init__(self, eid_instance_id, eid_instance_attribute, datatype, profile_id, display_name):
		eid_instance_id = str(eid_instance_id)
		self.insert_attrs_b = self.insert_attrs_b(eid_instance_id, eid_instance_attribute, datatype, str(profile_id))
		self.insert_attrs_tl_all = self.insert_attrs_tl_all(eid_instance_id, eid_instance_attribute, display_name)
		self.insert_attr_groups = self.insert_attr_groups(eid_instance_id, eid_instance_attribute)
		self.update_attr_groups = self.update_attr_groups(eid_instance_id, eid_instance_attribute)


	def insert_attrs_b(self, eid_instance_id, eid_instance_attribute, datatype, profile_id):
		table = 'FND_EID_PDR_ATTRS_B'
		column_headers = ['EID_INSTANCE_ID','EID_INSTANCE_ATTRIBUTE','ENDECA_DATATYPE', 'EID_ATTR_PROFILE_ID','EID_RELEASE_VERSION','ATTRIBUTE_SOURCE','MANAGED_ATTRIBUTE_FLAG','HIERARCHICAL_MGD_ATTR_FLAG', 'DIM_ENABLE_REFINEMENTS_FLAG','DIM_SEARCH_HIERARCHICAL_FLAG','REC_SEARCH_HIERARCHICAL_FLAG','MGD_ATTR_EID_RELEASE_VERSION','OBSOLETED_FLAG','OBSOLETED_EID_RELEASE_VERSION,CREATED_BY','CREATION_DATE','LAST_UPDATED_BY','LAST_UPDATE_DATE','LAST_UPDATE_LOGIN','ATTR_ENABLE_UPDATE_FLAG','VIEW_OBJECT_ATTR_NAME','ATTR_VALUE_SET_FLAG','VALUE_SET_NAME','ATTR_ENABLE_NULL_FLAG','DESCRIPTIVE_FLEXFIELD_NAME']
		values = [eid_instance_id, eid_instance_attribute, datatype, profile_id, '2.3', 'MSI','N','N','N','N','N','N','N','0','0','SYSDATE','0','SYSDATE','0','null','null','null','null','null','null']
		insert_statement = ''.join([SQL.INSERT_INTO, self.concat_schema_table(SQL.SCHEMA, table), self.create_column_name_string(*column_headers)])
		return ''.join([SQL.DEFINE_OFF, self.rem_insert_statement(SQL.SCHEMA, table), insert_statement, self.create_values_string(*values), SQL.COMMIT])


	def insert_attrs_tl(self, eid_instance_id ,eid_instance_attribute, language_code, display_name):
		table = 'FND_EID_PDR_ATTRS_TL'
		column_headers = ['EID_INSTANCE_ID','EID_INSTANCE_ATTRIBUTE','LANGUAGE','SOURCE_LANG','DISPLAY_NAME','ATTRIBUTE_DESC','USER_DISPLAY_NAME','USER_ATTRIBUTE_DESC,CREATED_BY','CREATION_DATE','LAST_UPDATED_BY','LAST_UPDATE_DATE','LAST_UPDATE_LOGIN']
		values = [eid_instance_id, eid_instance_attribute, language_code, 'US', display_name, display_name, display_name, display_name,'0', 'SYSDATE', '0', 'SYSDATE','0']
		insert_statement = ''.join([SQL.INSERT_INTO,self.concat_schema_table(SQL.SCHEMA, table),self.create_column_name_string(*column_headers)])        
		return ''.join([insert_statement, self.create_values_string(*values)])


#this method could use some TLC.
	def insert_attrs_tl_all(self, eid_instance_id, eid_instance_attribute, display_name):
		table = 'FND_EID_PDR_ATTRS_TL'
		statement = SQL.DEFINE_OFF + self.rem_insert_statement(SQL.SCHEMA, table)
		for l in SQL.EBS_LANGUAGE_CODES:
			language_statement = self.insert_attrs_tl(eid_instance_id, eid_instance_attribute, l, display_name)
			statement += language_statement + '\n'
		return ''.join([statement, '\n', SQL.COMMIT])


	def insert_attr_groups(self, eid_instance_id, eid_instance_attribute):
		table = 'FND_EID_ATTR_GROUPS'
		rem_insert_statement = self.rem_insert_statement(SQL.SCHEMA, table)
		column_headers = ['EID_INSTANCE_ID','EID_INSTANCE_GROUP','EID_INSTANCE_ATTRIBUTE','EID_INSTANCE_GROUP_ATTR_SEQ','EID_INST_GROUP_ATTR_USER_SEQ','GROUP_ATTRIBUTE_SOURCE','EID_RELEASE_VERSION','OBSOLETED_FLAG','OBSOLETED_EID_RELEASE_VERSION','CREATED_BY','CREATION_DATE','LAST_UPDATED_BY','LAST_UPDATE_DATE','LAST_UPDATE_LOGIN']
		insert_statement = ''.join([SQL.INSERT_INTO, self.concat_schema_table(SQL.SCHEMA, table), self.create_column_name_string(*column_headers)])        
		values = [eid_instance_id, 'Categories', eid_instance_attribute, '1', '1', 'MSI', '2.3', 'N', '0', '0', 'SYSDATE','0','SYSDATE','0']
		return ''.join([SQL.DEFINE_OFF, rem_insert_statement, insert_statement, self.create_values_string(*values), SQL.COMMIT])


	def update_attr_groups(self, eid_instance_id, eid_instance_attribute):
		table = 'FND_EID_ATTR_GROUPS'
		update = 'UPDATE ' + self.concat_schema_table(SQL.SCHEMA, table) + ' '
		set_statement = "SET EID_INSTANCE_GROUP_ATTR_SEQ = 1, EID_INST_GROUP_ATTR_USER_SEQ = 1 WHERE EID_INSTANCE_ID = "+eid_instance_id+" AND EID_INSTANCE_ATTRIBUTE = '"+ eid_instance_attribute +"'; \n"
		return ''.join([SQL.DEFINE_OFF, update, set_statement, SQL.COMMIT + '\n'])


	def rem_insert_statement(self, schema, table):
		return ''.join([SQL.REM_INSERT, self.concat_schema_table(schema, table), '\n'])


	def concat_schema_table(self, schema, table):
		return schema + '.' + table


	def create_column_name_string(self, *args):
		statement = ' (' + ''.join([a + ',' for a in args])
		statement = statement[0:-1]
		return statement + ')\n'


	def create_values_string(self, *args):
		statement = 'values ( '
		for a in args:
			if a == 'null' or a == 'SYSDATE' or a.isdigit():
				statement += a + ','
			else:
				statement += "'" + a +"'" + ','
		statement = statement[0:-1]
		return statement + ');'


	def save_sql(self):
		text = self.insert_attrs_b + '\n'+ self.insert_attrs_tl_all + '\n' + self.insert_attr_groups + '\n' + self.update_attr_groups
		with open('attribute_sql.txt', 'a') as f:
			f.write(text)


class Excel_Reader(object):

	def __init__(self):
		wb = openpyxl.load_workbook('endeca_attributes.xlsx')
		sheet = wb.get_sheet_by_name('endeca_attributes')
		highest_row = str(sheet.get_highest_row())
		self.attribute_data = []
		for rowOfCellObjects in sheet['A2': 'E'+ highest_row]:
			cell_data = [c.value for c in rowOfCellObjects]
			self.attribute_data.append(cell_data)

#not crazy about this at all. The idea is to clear the file prior to appending the sql statements
#totally a stopgap at the moment
	def clear_attribute_sql_file(self):
		open('attribute_sql.txt', 'w').close()


reader = Excel_Reader()
reader.clear_attribute_sql_file()
for r in reader.attribute_data:
	sql = SQL(*r)
   
sql.save_sql()