import book
import pytest
import library
import user

@pytest.mark.unit
def test_borrow_boo():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()
    assert book1.borrowed ==True

@pytest.mark.unit
def test_re_borrow_boo():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()
    assert book1.borrowed ==True
    with pytest.raises(ValueError, match="The book is already borrowed"):
        book1.borrow()
    
@pytest.mark.unit
def test__borrow_and_return_boo():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    assert book1.title == 'El alquimista'
    book1.borrow()
    assert book1.borrowed ==True
    book1.return_book()
    assert book1.borrowed ==False

@pytest.fixture
def library_init():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    miguel = user.User('Miguel', 'ID0001')
    
    lib = library.Library()
    lib.add_book(book1)
    lib.add_user(miguel)
    return lib
    

@pytest.mark.wip
def test_library_borrow_fixture(library_init):
    lib= library_init
    #comprobar si se guardo el usuario
    lib.borrow_book('ID0001', 'ISBN0001')
    assert lib.books[0].borrowed == True

@pytest.mark.sys
def test_library_borrowed1():
    book1 = book.Book('El alquimista', 'Paulo Coehlo', 1998, 'ISBN0001')
    miguel = user.User('Miguel', 'ID0001')

    lib = library.Library()
    lib.add_book(book1)
    assert lib.books[0].title == 'El alquimista'
    lib.add_user(miguel)
    #comprobar si se guardo el usuario
    lib.borrow_book('ID0001', 'ISBN0001')
    assert book1.borrowed == True