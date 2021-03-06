SELECT
RCTA.CUSTOMER_TRX_ID,
RCTA.PURCHASE_ORDER,

RCTLGDA.GL_DATE AS dt_revenue,

RCTLA.INTERFACE_LINE_ATTRIBUTE1 AS SALES_ORDER,

GCC.SEGMENT5 AS Wwapc,

OOHA.ATTRIBUTE1 AS SALES_OFFICE,

MSIB.SEGMENT1 AS PART_NUMBER

FROM APPS.RA_CUSTOMER_TRX_ALL RCTA

INNER JOIN

(
SELECT DISTINCT
RCTLGDA.GL_DATE, RCTLGDA.CUSTOMER_TRX_ID, RCTLGDA.CODE_COMBINATION_ID
FROM AR.RA_CUST_TRX_LINE_GL_DIST_ALL RCTLGDA
) RCTLGDA

ON RCTA.CUSTOMER_TRX_ID = RCTLGDA.CUSTOMER_TRX_ID

INNER JOIN APPS.RA_CUSTOMER_TRX_LINES_ALL RCTLA
ON RCTA.CUSTOMER_TRX_ID = RCTLA.CUSTOMER_TRX_ID

INNER JOIN APPS.GL_CODE_COMBINATIONS GCC
ON RCTLGDA.CODE_COMBINATION_ID = GCC.CODE_COMBINATION_ID

INNER JOIN APPS.OE_ORDER_HEADERS_ALL OOHA
ON RCTA.INTERFACE_HEADER_ATTRIBUTE1 =to_char(OOHA.ORDER_NUMBER)

INNER JOIN APPS.OE_ORDER_LINES_ALL OOLA
ON OOHA.HEADER_ID = OOLA.HEADER_ID

INNER JOIN APPS.OE_ORDER_SOURCES OOS
ON OOHA.ORDER_SOURCE_ID = OOS.ORDER_SOURCE_ID

INNER JOIN
(
SELECT OOHA.HEADER_ID,

HPS.PARTY_SITE_ID,

HZCA.CUST_ACCOUNT_ID,

HP.PERSON_FIRST_NAME ||' '|| HP.PERSON_LAST_NAME AS CONTACT_NAME,

HP.PARTY_NAME,

HL.ADDRESS1,HL.STATE, HL.COUNTRY

FROM APPS.OE_ORDER_HEADERS_ALL OOHA

INNER JOIN APPS.HZ_CUST_ACCOUNTS_ALL HZCA
ON OOHA.SHIP_TO_ORG_ID = HZCA.CUST_ACCOUNT_ID

INNER JOIN APPS.HZ_CUST_ACCT_SITES_ALL HCASA
ON HZCA.CUST_ACCOUNT_ID = HCASA.CUST_ACCOUNT_ID

INNER JOIN APPS.HZ_CUST_SITE_USES_ALL HCSUA
ON HCASA.CUST_ACCT_SITE_ID = HCSUA.CUST_ACCT_SITE_ID

INNER JOIN APPS.HZ_PARTY_SITES HPS
ON HCASA.PARTY_SITE_ID = HPS.PARTY_SITE_ID

INNER JOIN APPS.HZ_PARTIES HP
ON HPS.PARTY_ID = HP.PARTY_ID

INNER JOIN APPS.HZ_LOCATIONS HL
ON HPS.LOCATION_ID = HL.LOCATION_ID

WHERE HCSUA.PRIMARY_FLAG = 'Y'
AND HCSUA.SITE_USE_CODE = 'SHIP_TO') SHIP_TO

ON OOHA.HEADER_ID = SHIP_TO.HEADER_ID

INNER JOIN APPS.HZ_CUST_ACCOUNTS HCA
ON OOHA.SOLD_TO_ORG_ID =  HCA.CUST_ACCOUNT_ID


INNER JOIN APPS.MTL_SYSTEM_ITEMS_B MSIB
ON OOLA.INVENTORY_ITEM_ID = MSIB.INVENTORY_ITEM_ID


ORDER BY RCTLA.CUSTOMER_TRX_LINE_ID