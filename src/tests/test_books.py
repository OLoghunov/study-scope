booksPrefix = f"/api/0.1/books"


def testGetAllBooks(testClient, fakeBookService, fakeSession):
    response = testClient.get(
        url=f"{booksPrefix}",
    )

    assert fakeBookService.getAllBooksCalledOnce()
    assert fakeBookService.getAllBooksCalledOnceWith(fakeSession)