
DEFINE_OFF = 'SET DEFINE OFF;\n'
COMMIT = 'COMMIT;'


class SQL(object):
#need to add an attribute source as a parameter

    def __init__(self, eid_instance_id, eid_instance_attribute, datatype, profile_id, display_name):
		self.eid_instance_id = str(eid_instance_id)
		self.eid_instance_attribute = eid_instance_attribute
		self.datatype = datatype
		self.profile_id = str(profile_id)
		self.display_name = display_name
		self.insert_attrs_b = self.insert_attrs_b(self.eid_instance_id, self.eid_instance_attribute, self.datatype, self.profile_id)
		self.insert_attrs_tl_all = self.insert_attrs_tl_all(self.eid_instance_id, self.eid_instance_attribute, self.display_name)
		self.insert_attr_groups = self.insert_attr_groups(self.eid_instance_id, self.eid_instance_attribute)
		self.update_attr_groups = self.update_attr_groups(self.eid_instance_attribute)

    def insert_attrs_b(self, eid_instance_id, eid_instance_attribute, datatype, profile_id):
    	rem_insert_statement = 'REM INSERTING into APPS.FND_EID_PDR_ATTRS_B\n'
    	insert_statement = 'Insert into APPS.FND_EID_PDR_ATTRS_B (EID_INSTANCE_ID,EID_INSTANCE_ATTRIBUTE,ENDECA_DATATYPE, EID_ATTR_PROFILE_ID,EID_RELEASE_VERSION,ATTRIBUTE_SOURCE,MANAGED_ATTRIBUTE_FLAG,HIERARCHICAL_MGD_ATTR_FLAG, DIM_ENABLE_REFINEMENTS_FLAG,DIM_SEARCH_HIERARCHICAL_FLAG,REC_SEARCH_HIERARCHICAL_FLAG, MGD_ATTR_EID_RELEASE_VERSION,OBSOLETED_FLAG,OBSOLETED_EID_RELEASE_VERSION,CREATED_BY,CREATION_DATE, LAST_UPDATED_BY,LAST_UPDATE_DATE,LAST_UPDATE_LOGIN,ATTR_ENABLE_UPDATE_FLAG,VIEW_OBJECT_ATTR_NAME,ATTR_VALUE_SET_FLAG, VALUE_SET_NAME,ATTR_ENABLE_NULL_FLAG,DESCRIPTIVE_FLEXFIELD_NAME)\n'
    	values =  "("+ eid_instance_id +",'" + eid_instance_attribute + "','" + datatype + "'," + profile_id + ",'2.3','MSI','N','N','N','N','N','N','N','0',0,SYSDATE,0,SYSDATE,0,null,null,null,null,null,null);\n"
    	statement = DEFINE_OFF + rem_insert_statement + insert_statement + values + COMMIT
    	return statement


    def insert_attrs_tl(self, eid_instance_id ,eid_instance_attribute, language_code, display_name):
    	insert_statement = 'Insert into APPS.FND_EID_PDR_ATTRS_TL (EID_INSTANCE_ID,EID_INSTANCE_ATTRIBUTE,LANGUAGE,SOURCE_LANG,DISPLAY_NAME,ATTRIBUTE_DESC,USER_DISPLAY_NAME,USER_ATTRIBUTE_DESC,CREATED_BY,CREATION_DATE,LAST_UPDATED_BY,LAST_UPDATE_DATE,LAST_UPDATE_LOGIN) values'
    	values = "(" + eid_instance_id + ",'"+eid_instance_attribute+"','" + language_code + "','US','" + display_name + "','" + display_name +"','" + display_name + "','" + display_name + "',0,SYSDATE,0,SYSDATE,0);" 
    	statement = insert_statement + values 
    	return statement

    def insert_attrs_tl_all(self, eid_instance_id, eid_instance_attribute, display_name):
    	ebs_language_codes = ('D', 'DK', 'E', 'F', 'NL', 'PT', 'PTB', 'S', 'US', 'ZHS')
        rem_insert_statement = 'REM INSERTING into APPS.FND_EID_PDR_ATTRS_TL\n'
        statement = DEFINE_OFF + rem_insert_statement
        for l in ebs_language_codes:
        	language_statement = self.insert_attrs_tl(eid_instance_id, eid_instance_attribute, l, display_name)
        	statement += language_statement + '\n'
        return statement + '\n' + COMMIT 


    def insert_attr_groups(self, eid_instance_id, eid_instance_attribute):
    	rem_insert_statement = 'REM INSERTING into APPS.FND_EID_ATTR_GROUPS\n'
    	insert_statement = 'Insert into APPS.FND_EID_ATTR_GROUPS (EID_INSTANCE_ID,EID_INSTANCE_GROUP,EID_INSTANCE_ATTRIBUTE,EID_INSTANCE_GROUP_ATTR_SEQ,EID_INST_GROUP_ATTR_USER_SEQ,GROUP_ATTRIBUTE_SOURCE,EID_RELEASE_VERSION,OBSOLETED_FLAG,OBSOLETED_EID_RELEASE_VERSION,CREATED_BY,CREATION_DATE,LAST_UPDATED_BY,LAST_UPDATE_DATE,LAST_UPDATE_LOGIN) values '
    	values = "("+ eid_instance_id + ",'Categories','" +eid_instance_attribute + "',1,1,'MSI','2.3','N','0',0,SYSDATE,0,SYSDATE,0);"
    	statement = DEFINE_OFF + rem_insert_statement + insert_statement + values + COMMIT
    	return statement

    def update_attr_groups(self, eid_instance_attribute):
    	update = "UPDATE APPS.FND_EID_ATTR_GROUPS "
    	set_statement = "SET EID_INSTANCE_GROUP_ATTR_SEQ = 1, EID_INST_GROUP_ATTR_USER_SEQ = 1 WHERE EID_INSTANCE_ID = 14 AND EID_INSTANCE_ATTRIBUTE = '"+ eid_instance_attribute +"'; \n"
    	statement = DEFINE_OFF + update +  set_statement + COMMIT
    	return statement



sql = SQL(204, 'accounting_period', 'mdex:string', 1, 'Accounting Period')

print sql.update_attr_groups