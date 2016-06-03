
class XML(object):
	CLOSE_XML = '\n</Record>\n</Metadata>'
	ENDECA_TO_XML_LOOKUP = {'mdex:double' : 'number', 'mdex:string' : 'string', 'mdex:boolean' : 'boolean',
							'mdex:dateTime' : 'date', 'mdex:double' : 'decimal', 'mdex:int' : 'int',
							'mdex:long':'long'}

	def __init__(self, fields_datatypes_list, record_name):
		self.file = self.xml(self.metadata_id(id(self)), self.record_id(record_name), 
							 self.all_fields(fields_datatypes_list), XML.CLOSE_XML)
		

	def metadata_id(self, metadata_id):
		return  '<Metadata id="{}" previewAttachmentCharset="ISO-8859-1">\n'.format(metadata_id)


	def record_id(self, record_name):
		return r'<Record fieldDelimiter="|" name="{}" previewAttachmentCharset="ISO-8859-1" recordDelimiter="\r\n" recordSize="-1" type="delimited">\n'.format(record_name)


	def single_field(self, attribute_name, datatype):
		return '<Field name="'+attribute_name+'" type="'+ XML.ENDECA_TO_XML_LOOKUP[datatype]+'"/>'


	def all_fields(self, fields_and_datatypes):
		fields = [self.single_field(f[0], f[1]) for f in fields_and_datatypes]
		return '\n'.join(fields)


	def xml(self, metadata_id, record_id, fields, CLOSE_XML):
		return metadata_id + record_id + fields + CLOSE_XML


