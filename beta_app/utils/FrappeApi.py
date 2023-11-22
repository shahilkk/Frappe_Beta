import frappe
import requests
import json
headersList = {
                "Accept": "*/*",
                "User-Agent": "Khanal Tech",
                "Content-Type": "application/json" 
            }



#%%
import requests
#%%
headersList = {
                "Accept": "*/*",
                "User-Agent": "Khanal Tech",
                "Content-Type": "application/json" 
            }

# def Fetch_Data(num_books=20, **kwargs):
#     url = "https://frappe.io/api/method/frappe-library"
#     params = {'page': 1, 'num_books': num_books}

#     # Add additional parameters if provided
#     params.update(kwargs)

#     response = requests.get(url, params=params, headers=headersList, verify=False)

#     Frappe_Dict = dict(response.json())
#     # print(Frappe_Dict, 'Frappe_Dict')
#     book_count = len(Frappe_Dict.get('message', []))
#     print(f"Number of books with title '{kwargs}': {book_count}")
# def Fetch_Books(title, total_books=20):
#     url = "https://frappe.io/api/method/frappe-library"
#     page = 1
#     books_fetched = 0

#     while books_fetched < total_books:
#         params = {'page': page, 'title': title}
#         response = requests.get(url, params=params, headers=headersList, verify=False)

#         Frappe_Dict = dict(response.json())
#         books_on_page = Frappe_Dict.get('message', [])

#         # If no more books, break out of the loop
#         if not books_on_page:
#             break

#         # Process books on the current page
#         for book in books_on_page:
#             print(book)
#             books_fetched += 1

#         # Move to the next page
#         page += 1

#     # print(f"Total books fetched with title '{title}': {books_fetched}")
#     print(f"Number of books with title '{title}': {books_fetched}")



# %%
# Fetch_Books(title="Harry Potter", total_books=20)

# %%



import frappe
import requests

@frappe.whitelist()
def Fetch_Data(total_books=None, title=None):
    print(total_books,'total_books')
    print(title,'title')
    url = "https://frappe.io/api/method/frappe-library"
    start_page = 1
    page_count = int(start_page)
    
    while True:
        params      = {'page': page_count, 'title': title}
        response    = requests.get(url, params=params, headers=headersList, verify=False)
        
        Frappe_Dict     = dict(response.json())
        books_on_page   = Frappe_Dict.get('message', [])
        
        if not books_on_page:
            break  # No more books on the current page, exit the loop

        for Single_Books in books_on_page:
            try:
                doc                         = frappe.new_doc('Books')
                doc.book_id                 = Single_Books['bookID']
                doc.book_name               = Single_Books['title']
                doc.authors                 = Single_Books['authors']
                doc.average_rating          = Single_Books['average_rating']
                doc.isbn                    = Single_Books['isbn']
                doc.isbn13                  = Single_Books['isbn13']
                doc.num_pages               = Single_Books['  num_pages']
                doc.ratings_count           = Single_Books['ratings_count']
                doc.text_reviews_count      = Single_Books['text_reviews_count']
                doc.publication_date        = Single_Books['publication_date']
                doc.publisher               = Single_Books['publisher']
                doc.language                = Single_Books['language_code']
                doc.status                  = 'available'
                
                try:
                    doc.save()
                    frappe.db.commit()
                    # print(f"Book '{doc.book_name}' saved")
                except frappe.DuplicateEntryError:
                    pass
                    # print(f"Book '{doc.book_name}' already exists")
                
            except Exception as e:
                frappe.msgprint(f"Error processing book: {e}")

        page_count += 1  # Move to the next page

        if frappe.db.count('Books', {'book_name': ['like', f'%{title}%']}) >= int(total_books):
            frappe.msgprint(f"Number of books with title like '{title}': Reached {total_books}")
            break  # Exit the loop when the total_books limit is reached
    return frappe.msgprint(f"Number of books with title like '{title}': Saved {total_books}")


# bench --site beta.localhost execute  --args "('7','Harry Potter')"  beta_app.utils.FrappeApi.Fetch_Data


# {"Book":"Harry Potter and the Half-Blood Prince (Harry Potter  #6)","User":"shahilkhan.7139@gmail.com","Fromdate":"2023-11-08","Todate":"2023-11-24","fees":"400"}

@frappe.whitelist()
def issue_book(data):
    print(data,'data')
    data_dict = json.loads(data)
    # data_dict['PonumberDocentry']
    book = frappe.get_doc("Books",  data_dict['Book'])
    user = frappe.get_doc("Members",  data_dict['User'])
    print(user.money_to_pay,'user.money_to_pay')
    print(type(user.money_to_pay))

    if book.status == "available" and int(user.money_to_pay) <= 500:
        # Update Book status to "issued"
        book.status = "issued"
        book.save()
        newvalue = int(user.money_to_pay)  # Convert the current money_to_pay to an integer
        print(newvalue, 'newvalue')

        fees = int(data_dict['fees'])  # Convert the fees from the data_dict to an integer
        newvalue += fees  # Add the fees to newvalue
        print(newvalue, 'newvalue')

        user.money_to_pay = str(newvalue)  # Convert the updated value back to string before assigning it
        print(user.money_to_pay, 'user')

        user.save()
        # Create a new Transaction record
        transaction             = frappe.new_doc("Transactions")
        transaction.books       = data_dict['Book']
        transaction.members     = data_dict['User']
        transaction.from_date   = data_dict['Fromdate']
        transaction.to_date     = data_dict['Todate']
        transaction.fees        = data_dict['fees']
        transaction.save()
        frappe.db.commit()

        return "Book issued successfully"
    else:
        return "Book cannot be issued"


@frappe.whitelist()
def return_book(data):
    data_dict = json.loads(data)
    Transcation = frappe.get_doc("Transactions", data_dict['Transcation'])
    user = frappe.get_doc("Members", Transcation.members)
    print(user,'user')
    # transaction = frappe.get_doc("Transaction", {"book": book_name, "user": user_id})
    book = frappe.get_doc("Books",  Transcation.books)
    # Update Book status to "available"
    print(book,'book')
    book.status = "available"
    book.save()
    Transcation.paid=1
    Transcation.save()
    # Calculate rent fee and update outstanding debt
    # rent_fee = calculate_rent_fee(transaction)
    newvalue = int(user.money_to_pay)  # Convert the current money_to_pay to an integer
    print(newvalue, 'newvalue')

    fees = int(data_dict['fees'])  # Convert the fees from the data_dict to an integer
    newvalue -= fees  # Add the fees to newvalue
    print(newvalue, 'newvalue')

    user.money_to_pay = str(newvalue)  # Convert the updated value back to string before assigning it
    print(user.money_to_pay, 'user')
    user.save()
    frappe.db.commit()

    # Delete the Transaction record
    # frappe.delete_doc("Transaction", data_dict['Transcation'])

    return f"Book returned successfully. Rent fee: Rs. {data_dict['fees']}"
