from controladores.bd import obtener_conexion
import base64

tabla = 'producto'

def obtener_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id, 
                pr.nombre, 
                pr.price_regular, 
                pr.precio_online, 
                pr.precio_oferta, 
                pr.id, 
                pr.info_adicional, 
                pr.stock, 
                date(pr.fecha_registro), 
                pr.MARCAid, 
                pr.SUBCATEGORIAid,
                pr.disponibilidad
            FROM producto pr
            WHERE pr.id = %s
        '''
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def obtener_info_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id, 
                pr.nombre, 
                pr.price_regular, 
                pr.precio_online, 
                pr.precio_oferta, 
                pr.id, 
                pr.info_adicional, 
                pr.stock, 
                date(pr.fecha_registro), 
                pr.MARCAid, 
                pr.SUBCATEGORIAid,
                pr.disponibilidad,
                img.imagen,
                sub.categoriaid
            FROM producto pr
            LEFT JOIN img_producto img on img.PRODUCTOid = pr.id
            LEFT JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
            WHERE pr.id = %s AND img.imgPrincipal = 1
        '''
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()

    producto_elemento = None

    if producto:
        pro_id, nom, reg, onl , ofe , prod_id , pro_info , pro_st , pro_fec , pro_ma , pro_sub , pro_disp ,pro_img, cat_id = producto

        if pro_img:
            img_base64 = base64.b64encode(pro_img).decode('utf-8')
            img_url = f"data:image/png;base64,{img_base64}"
        else:
            img_url = ""  # Placeholder en caso de que no haya logo

        
    producto_elemento = (pro_id, nom, reg, onl , ofe , prod_id , pro_info , pro_st , pro_fec , pro_ma , pro_sub , pro_disp, img_url,cat_id)

    conexion.close()
    return producto_elemento


def ver_info_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id, 
                pr.nombre, 
                pr.price_regular, 
                pr.precio_online, 
                pr.precio_oferta, 
                pr.id, 
                pr.info_adicional, 
                pr.stock, 
                date(pr.fecha_registro), 
                pr.MARCAid, 
                pr.SUBCATEGORIAid,
                pr.disponibilidad,
                pr.id,
                sub.categoriaid
            FROM producto pr
            LEFT JOIN img_producto img on img.PRODUCTOid = pr.id
            LEFT JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
            WHERE pr.id = %s AND img.imgPrincipal = 1
        '''
        cursor.execute(sql, (id))
        producto = cursor.fetchone()
    conexion.close()
    return producto


def obtener_informacion_producto(id):
    return obtener_por_id(id)


def obtenerEnTarjetasTodos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen 
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                order by pr.fecha_registro desc;
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtenerEnTarjetasMasRecientes():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen,
                    sub.CATEGORIAid
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                order by pr.fecha_registro desc
                LIMIT 15
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cat_id= producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}",cat_id))
    
    conexion.close()
    return productos_lista


def obtenerEnTarjetasAlfabetico(orden):
    conexion = obtener_conexion()
    productos = []

    if orden == 0 :
        ordenar = 'asc'
    elif orden == 1: 
        ordenar = 'desc'

    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen,
                    sub.CATEGORIAid
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                order by pr.nombre '''+ordenar+'''
                LIMIT 15
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cat_id= producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}",cat_id))
    
    conexion.close()
    return productos_lista


def obtenerEnTarjetasxPrecio(orden):
    conexion = obtener_conexion()
    productos = []

    if orden == 0 :
        ordenar = 'asc'
    elif orden == 1: 
        ordenar = 'desc'

    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen,
                    sub.CATEGORIAid
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                order by pr.precio_oferta '''+ordenar+''' ,  pr.precio_online '''+ordenar+'''
                LIMIT 15
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cat_id= producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}",cat_id))
    
    conexion.close()
    return productos_lista




def buscarEnTarjetasMasRecientes(nombre):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen,
                    sub.CATEGORIAid
                FROM producto pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                and ( UPPER(pr.nombre) LIKE UPPER('%'''+str(nombre)+'''%') or UPPER(mar.marca) LIKE UPPER('%'''+str(nombre)+'''%'))
                order by pr.fecha_registro desc
                LIMIT 15
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cat_id= producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}",cat_id))
    
    conexion.close()
    return productos_lista


def obtenerEnTarjetasMasPopulares_catalogo():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen,
                    SUM(dp.cantidad) AS total_compras
                FROM 
                    producto pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                left JOIN detalles_pedido dp ON pr.id = dp.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                GROUP BY 
                    pr.id
                ORDER BY total_compras DESC , pr.fecha_registro desc
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cant = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtenerEnTarjetasMasPopulares():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen,
                    SUM(dp.cantidad) AS total_compras
                FROM 
                    producto pr
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN detalles_pedido dp ON pr.id = dp.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and mar.disponibilidad = 1
                and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                GROUP BY 
                    pr.id
                ORDER BY 
                    total_compras DESC
                LIMIT 15;
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cant = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtenerEnTarjetasOfertas():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen 
                FROM `producto` pr 
                inner join img_producto ipr on pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.subcategoriaid
                INNER JOIN categoria cat on cat.id = sub.categoriaid
                INNER JOIN marca mar on mar.id = pr.marcaid
                WHERE cat.disponibilidad = 1 and sub.disponibilidad = 1 and ipr.imgPrincipal = 1 and pr.disponibilidad = 1 
                and mar.disponibilidad = 1 and pr.precio_oferta > 0
                order by pr.fecha_registro desc
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtener_en_tarjetas_marca(id,marca, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen ,
                    sub.categoriaid
                FROM producto pr 
                INNER JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' AND pr.MARCAid = '''+str(marca)+'''
                ORDER BY pr.fecha_registro desc
            '''
        
        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cat_id= producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""

        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}",cat_id))
    
    conexion.close()
    return productos_lista


def obtener_en_tarjetas_subcategoria(id,subcategoria, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen 
                FROM producto pr 
                INNER JOIN img_producto ipr 
                ON pr.id = ipr.PRODUCTOid 
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' AND pr.SUBCATEGORIAid = '''+str(subcategoria)+'''
                ORDER BY pr.fecha_registro desc
            '''
        
        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""

        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}"))
    
    conexion.close()
    return productos_lista


def obtener_en_tarjetas_categoria(id,categoria, limit):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,  
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid, 
                    ipr.imagen,
                    sub.categoriaid
                FROM producto pr 
                INNER JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid
                INNER JOIN subcategoria sub on sub.id = pr.SUBCATEGORIAid
                WHERE ipr.imgPrincipal = 1 AND pr.disponibilidad = 1 AND pr.id != '''+str(id)+''' 
                AND sub.CATEGORIAid = '''+str(categoria)+'''
                ORDER BY pr.fecha_registro desc
            '''
        
        if limit > 0:
            sql += ''' LIMIT '''+str(limit)

        cursor.execute(sql)
        productos = cursor.fetchall()
    
    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, img_binario , cat_id = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""

        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_mar, pr_sub, f"data:image/png;base64,{img_url}",cat_id))
    
    conexion.close()
    return productos_lista


# CRUD

def insertar_producto(nombre, price_regular, price_online, precio_oferta, info_adicional, stock, marca_id, subcategoria_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            INSERT INTO producto(nombre, price_regular, precio_online, precio_oferta, info_adicional, stock, disponibilidad, MARCAid, SUBCATEGORIAid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, info_adicional, stock, 1, marca_id, subcategoria_id))

        cursor.execute('SELECT LAST_INSERT_ID();')
        id_producto = cursor.fetchone()[0]

    conexion.commit()
    conexion.close()

    return id_producto


def obtener_productos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                id, 
                nombre, 
                price_regular, 
                precio_online, 
                precio_oferta, 
                id, 
                info_adicional, 
                stock, 
                date(fecha_registro), 
                disponibilidad,
                MARCAid, 
                SUBCATEGORIAid 
            FROM producto
        '''
        cursor.execute(sql)
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_listado_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,
                    pr.id,
                    pr.info_adicional, 
                    pr.stock, 
                    date(pr.fecha_registro), 
                    pr.disponibilidad,
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.disponibilidad,
                    cat.disponibilidad,
                    mar.disponibilidad,
                    count(car.caracteristicaid),
                    COALESCE(img_count.total_imagenes, 0) AS total_imagenes
                FROM `producto` pr 
                LEFT JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid AND ipr.imgPrincipal = 1
                LEFT JOIN subcategoria sub ON sub.id = pr.subcategoriaid
                LEFT JOIN categoria cat ON cat.id = sub.categoriaid
                LEFT JOIN marca mar ON mar.id = pr.marcaid
                left join caracteristica_producto car on car.productoid = pr.id
                LEFT JOIN (
                                SELECT 
                                    PRODUCTOid, 
                                    COUNT(*) AS total_imagenes 
                                FROM img_producto 
                                GROUP BY PRODUCTOid
                            ) AS img_count ON pr.id = img_count.PRODUCTOid
                GROUP BY pr.id;
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_id, pr_info, pr_stock, pr_fec, pr_disp,pr_mar, pr_sub, img_binario , sub_disp , cat_disp , mar_disp , cant_car , cant_img = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_id, pr_info, pr_stock, pr_fec, pr_disp,pr_mar, pr_sub, f"data:image/png;base64,{img_url}" , sub_disp , cat_disp , mar_disp , cant_car , cant_img))
    
    conexion.close()
    return productos_lista


def buscar_listado_productos_nombre(nombre):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = '''
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    pr.price_regular, 
                    pr.precio_online, 
                    pr.precio_oferta,
                    pr.id,
                    pr.info_adicional, 
                    pr.stock, 
                    date(pr.fecha_registro), 
                    pr.disponibilidad,
                    pr.MARCAid, 
                    pr.SUBCATEGORIAid,
                    ipr.imagen,
                    sub.disponibilidad,
                    cat.disponibilidad,
                    mar.disponibilidad,
                    count(car.caracteristicaid),
                    COALESCE(img_count.total_imagenes, 0) AS total_imagenes
                FROM `producto` pr 
                LEFT JOIN img_producto ipr ON pr.id = ipr.PRODUCTOid AND ipr.imgPrincipal = 1
                LEFT JOIN subcategoria sub ON sub.id = pr.subcategoriaid
                LEFT JOIN categoria cat ON cat.id = sub.categoriaid
                LEFT JOIN marca mar ON mar.id = pr.marcaid
                left join caracteristica_producto car on car.productoid = pr.id
                LEFT JOIN (
                                SELECT 
                                    PRODUCTOid, 
                                    COUNT(*) AS total_imagenes 
                                FROM img_producto 
                                GROUP BY PRODUCTOid
                            ) AS img_count ON pr.id = img_count.PRODUCTOid
                where ipr.imgPrincipal = 1 and UPPER(pr.nombre) LIKE UPPER ('%'''+str(nombre)+'''%')
                GROUP BY pr.id
                order by pr.nombre
            '''
        cursor.execute(sql)
        productos = cursor.fetchall()

    productos_lista = []
    for producto in productos:
        pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_id, pr_info, pr_stock, pr_fec, pr_disp,pr_mar, pr_sub, img_binario , sub_disp , cat_disp , mar_disp , cant_car , cant_img = producto
        img_url = base64.b64encode(img_binario).decode('utf-8') if img_binario else ""
        productos_lista.append((pr_id, pr_nombre, pr_reg, pr_on, pr_of, pr_id, pr_info, pr_stock, pr_fec, pr_disp,pr_mar, pr_sub, f"data:image/png;base64,{img_url}" , sub_disp , cat_disp , mar_disp , cant_car , cant_img))
    
    conexion.close()
    return productos_lista


def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM producto WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()


def actualizar_producto(nombre, price_regular, price_online, precio_oferta, info_adicional, stock, disponibilidad, marca_id, subcategoria_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            UPDATE producto 
            SET nombre = %s, price_regular = %s, precio_online = %s, precio_oferta = %s, info_adicional = %s, stock = %s, disponibilidad = %s, MARCAid = %s, SUBCATEGORIAid = %s 
            WHERE id = %s
        '''
        cursor.execute(sql, (nombre, price_regular, price_online, precio_oferta, info_adicional, stock, disponibilidad, marca_id, subcategoria_id, id))
    conexion.commit()
    conexion.close()


def obtener_por_nombre(nombre):
    conexion = obtener_conexion()
    producto = []
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id, 
                pr.nombre, 
                pr.price_regular, 
                pr.precio_online, 
                pr.precio_oferta, 
                pr.id, 
                pr.info_adicional, 
                pr.stock, 
                date(pr.fecha_registro), 
                pr.MARCAid, 
                pr.SUBCATEGORIAid,
                pr.disponibilidad
            FROM producto pr
            WHERE pr.nombre LIKE '%'''+str(nombre)+'''%' and pr.disponibilidad = 1
        '''
        cursor.execute(sql)
        producto = cursor.fetchall()
    conexion.close()
    return producto




##validar las eliminaciones físicas

def buscar_en_caracteristica_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM caracteristica_producto WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result


def buscar_en_img_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM img_producto WHERE PRODUCTOid = %s and imgPrincipal = 0", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result


def buscar_en_lista_deseos(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM lista_deseos WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result


def buscar_en_detalles_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM detalles_pedido WHERE PRODUCTOid = %s", (id,))
        result = cursor.fetchone()
    conexion.close()
    return result



