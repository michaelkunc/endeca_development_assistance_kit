
class XML(object):
	CLOSE_XML = '\n</Record>\n</Metadata>'
	ENDECA_TO_XML_LOOKUP = {'mdex:double' : 'number', 'mdex:string' : 'string', 'mdex:boolean' : 'boolean',
							'mdex:dateTime' : 'date', 'mdex:int' : 'integer',
							'mdex:long':'long'}

	def __init__(self, field_names_and_datatypes, record_name):
		self.record_name = record_name
		self.field_names_and_datatypes = field_names_and_datatypes

	def metadata_id(self, metadata_id):
		return  '<Metadata id="{}" previewAttachmentCharset="ISO-8859-1">\n'.format(metadata_id)


	def record_id(self, record_name):
		return r'<Record fieldDelimiter="|" name="{}" previewAttachmentCharset="ISO-8859-1" recordDelimiter="\r\n" recordSize="-1" type="delimited">\n'.format(record_name)


	def validate_data_types(self):
		data_types = [f[1] for f in self.field_names_and_datatypes]
		return set(data_types).issubset(XML.ENDECA_TO_XML_LOOKUP.keys())


	def single_field(self, attribute_name, datatype):
		return '<Field name="'+attribute_name+'" type="'+ XML.ENDECA_TO_XML_LOOKUP[datatype]+'"/>'


	def all_fields(self, fields_and_datatypes):
		fields = [self.single_field(f[0], f[1]) for f in fields_and_datatypes]
		return '\n'.join(fields)


	def generate_xml(self):
		return self.metadata_id(id(self)) + self.record_id(self.record_name) + self.all_fields(self.field_names_and_datatypes) + self.CLOSE_XML
