import book      # importa el modulo book.py (clase Book)
import pytest    # importa pytest (marcadores, fixtures, raises, parametrize)
import library   # importa el modulo library.py (clase Library y dict settings)
import user      # importa el modulo user.py (clase User)


# ============================================================
# TEMA: Marcadores de pytest (@pytest.mark.unit)
# ============================================================
@pytest.mark.unit  # asigna el marcador "unit" a esta prueba
def test_borrow_boo():
    # crea un libro con titulo, autor, anio e isbn
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    # verifica que el titulo se guardo bien
    assert book1.title == 'El alquimista'
    # presta el libro (borrowed pasa a True)
    book1.borrow()
    # verifica que quedo marcado como prestado
    assert book1.borrowed == True


# ============================================================
# TEMA: pytest.raises() con match (mensaje de la excepcion)
# ============================================================
@pytest.mark.unit
def test_re_borrow_boo():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    assert book1.title == 'El alquimista'
    # primer prestamo, funciona normal
    book1.borrow()
    assert book1.borrowed == True
    # segundo prestamo: debe lanzar ValueError con ese mensaje exacto
    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()  # esta linea es la que provoca la excepcion


# ============================================================
# TEMA: Prueba unitaria basica (flujo prestar y devolver)
# ============================================================
@pytest.mark.unit
def test__borrow_and_return_boo():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()                     # lo presta
    assert book1.borrowed == True      # comprueba que esta prestado
    book1.return_book()                # lo devuelve
    assert book1.borrowed == False     # comprueba que ya no esta prestado


# ============================================================
# TEMA: Fixtures (@pytest.fixture)
# Datos repetidos (libro, usuario, biblioteca) en un solo lugar
# ============================================================
@pytest.fixture  # marca la funcion como fixture, pytest la ejecuta antes de cada prueba que la pida
def library_init():
    # crea un libro de prueba
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    # crea un usuario de prueba
    miguel = user.User('Miguel', 'ID0001')

    lib = library.Library()   # crea la biblioteca vacia
    lib.add_book(book1)       # le agrega el libro
    lib.add_user(miguel)      # le agrega el usuario
    return lib                # entrega la biblioteca lista a la prueba


# TEMA: Fixtures + Marcadores (la fixture se pide como argumento)
@pytest.mark.wip  # marcador "wip"
def test_library_borrow_fixture(library_init):  # library_init llega como argumento
    lib = library_init                          # guarda la biblioteca en una variable
    lib.borrow_book('ID0001', 'ISBN0001')       # el usuario ID0001 presta el libro ISBN0001
    assert lib.books[0].borrowed == True        # verifica que el libro quedo prestado


# TEMA: Fixtures (segunda prueba que reutiliza la misma fixture)
@pytest.mark.wip
def test_library_has_data_fixture(library_init):
    # verifica que el libro se guardo en la biblioteca
    assert library_init.books[0].title == 'El alquimista'
    # verifica que el usuario se guardo en la biblioteca
    assert library_init.users[0].name == 'Miguel'


# TEMA: Fixtures (tercera prueba) + cobertura de Library.return_book
@pytest.mark.wip
def test_library_borrow_and_return_fixture(library_init):
    lib = library_init
    lib.borrow_book('ID0001', 'ISBN0001')            # presta el libro
    assert lib.books[0].borrowed == True             # confirma que esta prestado
    lib.return_book('ID0001', 'ISBN0001')            # lo devuelve
    assert lib.books[0].borrowed == False            # confirma que ya no esta prestado
    assert len(lib.users[0].get_history()) == 2      # historial del usuario: 1 prestamo + 1 devolucion


# ============================================================
# TEMA: Marcadores (prueba de sistema, sin fixture)
# ============================================================
@pytest.mark.sys  # marcador "sys" (prueba de sistema)
def test_library_borrowed1():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    miguel = user.User('Miguel', 'ID0001')

    lib = library.Library()
    lib.add_book(book1)                              # agrega el libro
    assert lib.books[0].title == 'El alquimista'     # verifica que se agrego
    lib.add_user(miguel)                             # agrega el usuario
    lib.borrow_book('ID0001', 'ISBN0001')            # presta el libro
    assert book1.borrowed == True                    # verifica que quedo prestado


# ============================================================
# TEMA: Parametrize (@pytest.mark.parametrize)
# Una sola funcion de prueba que corre 3 veces con datos distintos
# ============================================================
@pytest.mark.unit
@pytest.mark.parametrize("title, author, year, isbn", [  # nombres de los parametros de entrada
    ("El alquimista", "Paulo Coehlo", 1998, "ISBN0001"),  # caso 1
    ("Pedro Paramo", "Juan Rulfo", 1955, "ISBN0002"),     # caso 2
    ("Rayuela", "Julio Cortazar", 1963, "ISBN0003"),      # caso 3
])
def test_book_creation_parametrize(title, author, year, isbn):  # recibe los datos de cada caso
    b = book.Book(title, author, year, isbn)  # crea el libro con los datos del caso
    assert b.title == title                   # el titulo debe coincidir
    assert b.author == author                 # el autor debe coincidir
    assert b.year == year                     # el anio debe coincidir
    assert b.isbn == isbn                     # el isbn debe coincidir
    assert b.borrowed == False                # un libro nuevo no esta prestado


# ============================================================
# TEMA: monkeypatch.setattr()
# Reemplazo temporal de un metodo por una funcion falsa
# ============================================================
@pytest.mark.unit
def test_monkeypatch_setattr_borrow(monkeypatch, library_init):  # monkeypatch es fixture de pytest
    llamadas = []  # lista para registrar cuando se llame la funcion falsa

    def fake_borrow(self):              # funcion falsa que sustituye a Book.borrow
        llamadas.append(self.title)     # guarda el titulo para saber que se llamo
        self.borrowed = True            # simula el prestamo

    # sustituye Book.borrow por fake_borrow SOLO durante esta prueba
    monkeypatch.setattr(book.Book, "borrow", fake_borrow)
    library_init.borrow_book('ID0001', 'ISBN0001')    # Library llama a book.borrow() (que ahora es la falsa)
    assert llamadas == ['El alquimista']              # comprueba que la funcion falsa si se ejecuto
    assert library_init.books[0].borrowed == True     # comprueba el resultado esperado


# ============================================================
# TEMA: monkeypatch.delattr()
# Elimino temporalmente "settings" del modulo library
# ============================================================
@pytest.mark.unit
def test_monkeypatch_delattr_settings(monkeypatch, library_init):
    # borra la variable settings del modulo library durante esta prueba
    monkeypatch.delattr(library, "settings")
    # borrow_book usa settings, y como ya no existe debe lanzar NameError
    with pytest.raises(NameError):
        library_init.borrow_book('ID0001', 'ISBN0001')


# ============================================================
# TEMA: monkeypatch.setitem()
# Cambio temporal de un valor en el diccionario settings
# ============================================================
@pytest.mark.config  # marcador "config"
def test_monkeypatch_setitem_loans_disabled(monkeypatch, library_init):
    # cambia settings["loans_enabled"] a False solo durante esta prueba
    monkeypatch.setitem(library.settings, "loans_enabled", False)
    library_init.borrow_book('ID0001', 'ISBN0001')    # intenta prestar con prestamos apagados
    # como estan deshabilitados, el libro NO debe quedar prestado
    assert library_init.books[0].borrowed == False


# ============================================================
# TEMA: capsys
# Captura de lo que la funcion imprime en pantalla
# ============================================================
@pytest.mark.config
def test_capsys_loans_disabled(monkeypatch, capsys, library_init):  # capsys captura stdout
    # apaga los prestamos para que se ejecute el print
    monkeypatch.setitem(library.settings, "loans_enabled", False)
    library_init.borrow_book('ID0001', 'ISBN0001')    # aqui se ejecuta print("Loans are disabled")
    captured = capsys.readouterr()                    # lee lo que se imprimio
    assert captured.out == "Loans are disabled\n"     # compara captured.out (print agrega el \n)


# ============================================================
# TEMA: pytest.raises()
# Excepciones especificas cuando la entrada es invalida
# ============================================================
@pytest.mark.unit
def test_return_book_not_borrowed():
    b = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    # devolver un libro que nunca se presto debe lanzar ValueError
    with pytest.raises(ValueError, match="The book is not currently borrowed"):
        b.return_book()


@pytest.mark.unit
def test_borrow_book_not_found(library_init):
    # isbn que no existe en la biblioteca: debe lanzar ValueError
    with pytest.raises(ValueError, match="Book not found"):
        library_init.borrow_book('ID0001', 'ISBN9999')


@pytest.mark.unit
def test_borrow_user_not_found(library_init):
    # usuario que no existe en la biblioteca: debe lanzar ValueError
    with pytest.raises(ValueError, match="User not found"):
        library_init.borrow_book('ID9999', 'ISBN0001')


# ============================================================
# TEMA: try-except
# safe_borrow_book captura ValueError, pero NO captura AttributeError
# ============================================================
@pytest.mark.unit
def test_safe_borrow_success(library_init):
    # caso sin error: el try se ejecuta completo y regresa el mensaje de exito
    assert library_init.safe_borrow_book('ID0001', 'ISBN0001') == "Loan successful"


@pytest.mark.unit
def test_safe_borrow_catches_valueerror(library_init):
    library_init.safe_borrow_book('ID0001', 'ISBN0001')            # primer prestamo, funciona
    result = library_init.safe_borrow_book('ID0001', 'ISBN0001')   # segundo prestamo: ValueError
    # el except lo captura (no se propaga) y regresa el mensaje de error
    assert result == "Error: The book is already borrowed"


@pytest.mark.unit
def test_safe_borrow_propagates_attributeerror(monkeypatch, library_init):
    # elimina register_borrow de User para provocar un AttributeError
    monkeypatch.delattr(user.User, "register_borrow")
    # AttributeError no esta en el except (solo ValueError), entonces se propaga
    with pytest.raises(AttributeError):
        library_init.safe_borrow_book('ID0001', 'ISBN0001')


# ============================================================
# TEMA: Cobertura de caja blanca (--cov, term-missing)
# Cubre lineas que salian en Missing: Library.return_book,
# User.register_return y User.get_history
# ============================================================
@pytest.mark.unit
def test_user_history(library_init):
    library_init.borrow_book('ID0001', 'ISBN0001')     # genera la entrada de prestamo en el historial
    library_init.return_book('ID0001', 'ISBN0001')     # genera la entrada de devolucion (linea que no se cubria)
    history = library_init.users[0].get_history()      # obtiene el historial del usuario
    assert len(history) == 2                           # debe haber 2 registros
    assert "El alquimista" in history[0]               # el 1ro menciona el libro
    assert "El alquimista" in history[1]               # el 2do menciona el libro