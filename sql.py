QUERY_PORTFOLIO = """SELECT SUM(VALUE) AS PORTFOLIO, FECHA, WEEK(FECHA) AS WEEK FROM KPI.KPI_PORTFOLIO WHERE
(FECHA>'2023-01-01' AND DATE_PART('weekday',FECHA)=0) OR FECHA=CURRENT_DATE
group by FECHA
"""

QUERY_SOLAR_SALES = """SELECT SUM(VALUE) AS SOLAR_SALES, WEEK FROM(
select sum(value) as value, WEEK from(
select to_date(sale_date) AS SALE_DATE, count(*) as VALUE, WEEK(SALE_DATE) AS WEEK from SOLAR.CON_SCONTRACT_DIM
where is_sell = 1 and sales_segment in('D2D', 'VIDEOCALL', 'INDIRECT_CHANNEL', 'OTHERS')
AND SALE_DATE>'2023-01-01' AND SALE_DATE <= CURRENT_DATE
group by sale_date
order by to_date(sale_date) desc)
GROUP BY SALE_DATE, WEEK)
GROUP BY WEEK
"""

QUERY_SOLAR_INSTALLATIONS = """SELECT SUM(VALUE) AS SOLAR_INSTALLATIONS, WEEK(FECHA) AS WEEK FROM KPI.KPI_INSTALLATIONS
WHERE KPI_DESC = 'Notificada'
  AND FECHA>'2023-01-01'
group by WEEK
"""

QUERY_CLOUD_SALES = """SELECT SUM(VALUE) AS CLOUD_SALES, WEEK(FECHA) AS WEEK FROM KPI.KPI_SALES
WHERE KPI_DESC='Venta Cloud'
  AND FECHA>'2023-01-01'
group by WEEK
"""

QUERY_PORTFOLIO_LAST15_DAYS = """SELECT SUM(VALUE) AS PORTFOLIO, FECHA FROM KPI.KPI_PORTFOLIO WHERE
FECHA BETWEEN CURRENT_DATE-15 AND CURRENT_DATE
GROUP BY FECHA
ORDER BY FECHA
"""

QUERY_PORTFOLIO_PRODUCT = """SELECT SUM(VALUE) AS PORTFOLIO, PRODUCT_CLASSIFICATION FROM KPI.KPI_PORTFOLIO
WHERE FECHA=(SELECT MAX(FECHA) FROM KPI.KPI_PORTFOLIO) AND PRODUCT_CLASSIFICATION IS NOT NULL
GROUP BY PRODUCT_CLASSIFICATION
"""

QUERY_PORTFOLIO_MAPS = """SELECT A.CUPS, B.COORD_X AS LON, B.COORD_Y AS LAT FROM
    (SELECT DISTINCT CUPS FROM CON_ECONTRACT_DIM WHERE CO_STATUS_ID<10) A
LEFT JOIN PSE_NORMALIZED_ADDRESSES_DIM B ON A.CUPS=B.CUPS"""

QUERY_SOLAR_SALES_LAST15DAYS = """select sum(value) as SOLAR_SALES, SALE_DATE from(
            select to_date(sale_date) AS SALE_DATE, count(*) as VALUE from SOLAR.CON_SCONTRACT_DIM
            where is_sell = 1 and sales_segment in('D2D', 'VIDEOCALL', 'INDIRECT_CHANNEL', 'OTHERS')
              AND SALE_DATE BETWEEN CURRENT_DATE-15 AND CURRENT_DATE
            group by sale_date
            order by to_date(sale_date) desc)
     GROUP BY SALE_DATE ORDER BY SALE_DATE
"""

QUERY_SOLAR_SALES_2023 = """select sum(value) as SOLAR_SALES from(
    select to_date(sale_date) AS SALE_DATE, count(*) as VALUE from SOLAR.CON_SCONTRACT_DIM
    where is_sell = 1 and sales_segment in('D2D', 'VIDEOCALL', 'INDIRECT_CHANNEL', 'OTHERS')
      AND SALE_DATE BETWEEN '2023-01-01' AND CURRENT_DATE
    group by sale_date
    order by to_date(sale_date) desc)
    """

QUERY_SOLAR_SALES_MAP = """SELECT A.CUPS, A.SALE_DATE, B.COORD_X AS LON, B.COORD_Y AS LAT FROM
    (select to_date(sale_date) AS SALE_DATE, CUPS from SOLAR.CON_SCONTRACT_DIM
     where is_sell = 1 and sales_segment in('D2D', 'VIDEOCALL', 'INDIRECT_CHANNEL', 'OTHERS')
       AND SALE_DATE BETWEEN CURRENT_DATE-15 AND CURRENT_DATE
     order by to_date(sale_date) desc) A
        LEFT JOIN PSE_NORMALIZED_ADDRESSES_DIM B ON A.CUPS=B.CUPS
    """

QUERY_SOLAR_INSTALLATIONS_2023 = """SELECT SUM(VALUE) AS SOLAR_INSTALLATIONS FROM KPI.KPI_INSTALLATIONS
WHERE KPI_DESC = 'Notificada'
  AND FECHA>='2023-01-01'
"""

QUERY_SOLAR_INSTALLATIONS_LAST15 = """SELECT SUM(VALUE) AS SOLAR_INSTALLATIONS, FECHA FROM KPI.KPI_INSTALLATIONS
WHERE KPI_DESC = 'Realizada'
  AND FECHA BETWEEN CURRENT_DATE-15 AND CURRENT_DATE
group by FECHA
ORDER BY FECHA
"""

QUERY_CLOUD_SALES_LAST15 = """SELECT SUM(VALUE) AS CLOUD_SALES, FECHA FROM KPI.KPI_SALES
WHERE KPI_DESC='Venta Cloud'
  AND FECHA BETWEEN CURRENT_DATE-15 AND CURRENT_DATE
group by FECHA ORDER BY FECHA
"""

QUERY_CLOUD_SALES_2023 = """SELECT SUM(VALUE) AS CLOUD_SALES FROM KPI.KPI_SALES
WHERE KPI_DESC='Venta Cloud'
  AND FECHA>='2023-01-01'
"""

QUERY_CLOUD_SALES_MAP = """SELECT A.CUPS, A.FECHA AS SALE_DATE, B.COORD_X AS LON, B.COORD_Y AS LAT FROM(
SELECT DISTINCT A.CUPS AS CUPS,
                TO_DATE(A.CLOUD_CONTRACT_SIGNATURE_DATE) AS FECHA
FROM
    (SELECT * FROM SOLAR.CON_SCONTRACT_DIM WHERE PRODUCT = 'Cloud' AND CURRENT_PHASE IN ('Contrato Cloud Firmado','Servicio Cloud Activo')
    ) A
        LEFT JOIN (SELECT * FROM CON_ECONTRACT_DIM WHERE CO_STATUS_ID=1) B ON A.CUPS = B.CUPS
WHERE TO_DATE(A.CLOUD_CONTRACT_SIGNATURE_DATE)  <= CURRENT_DATE
  AND TO_DATE(A.CLOUD_CONTRACT_SIGNATURE_DATE)>=DATEADD(DAY, -15, CURRENT_DATE())
  AND B.CO_STATUS_ID=1) A
LEFT JOIN PSE_NORMALIZED_ADDRESSES_DIM B ON A.CUPS=B.CUPS
"""