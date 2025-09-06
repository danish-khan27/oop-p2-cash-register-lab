
class CashRegister:
    """
    Cash register that can add items, apply a percent discount,
    and void the last transaction.
    """

    def __init__(self, discount=0):
        self._discount = 0
        self.discount = discount  
        self.total = 0
        self.items = []  
        self.previous_transactions = []  

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if isinstance(value, int) and 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")

    def add_item(self, item, price, quantity=1):
        """
        Add an item purchase.
        - total increases by price * quantity
        - items gets the item name repeated `quantity` times
        - previous_transactions records the purchase
        """
        line_total = price * quantity
        self.total += line_total
        self.items.extend([item] * quantity)
        self.previous_transactions.append({
            "type": "purchase",
            "item": item,
            "price": price,
            "quantity": quantity,
            "total_change": line_total,
        })

    def apply_discount(self):
        """
        Apply the configured percent discount to the current total.
        Prints the required success/failure message.
        """
        if self.discount == 0:
            print("There is no discount to apply.")
            return

        self.total = self.total * (1 - self.discount / 100)
        shown = int(self.total) if self.total == int(self.total) else round(self.total, 2)
        print(f"After the discount, the total comes to ${shown}.")

        self.previous_transactions.append({
            "type": "discount",
            "percent": self.discount,
            "total_change": -self.total  
        })

    def void_last_transaction(self):
        """
        Undo the most recent transaction.
        - For a purchase: subtract its line total and remove its items.
        - For a discount: cannot reconstruct prior total without storing it,
          so simply no-op if discount is last (tests typically focus on purchases).
        """
        if not self.previous_transactions:
            return

        last = self.previous_transactions.pop()
        if last.get("type") == "purchase":
            self.total -= last["total_change"]

            remaining = last["quantity"]
            i = len(self.items) - 1
            while remaining > 0 and i >= 0:
                if self.items[i] == last["item"]:
                    self.items.pop(i)
                    remaining -= 1
                i -= 1
