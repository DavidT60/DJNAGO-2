from random import randint
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

  wait_time = between(1, 5) # 1 seconds to 5 seconds random #  

  @task(1)
  def view_products(self):
       collection_id = randint(1,4) 
       self.client.get(f'/store/product?collection_id={collection_id}', name='/store/product')
       
  @task(4)
  def view_product(self):
      product_id = randint(1,20)
      self.client.get(f'/store/product/{product_id}', name='/store/product/:id')
 
  @task(3)
  def add_product_cart(self):
       product_id = randint(1,20)
       product_cart = self.cart_id
       self.client.post(f'/store/cart/{product_cart}/cartitems/', name='cartitems', json={ "product":product_id, "quantity": 12})
      
  def on_start(self):
      response = self.client.post(f'/store/cart/', name='new user')
      json_result = response.json() # Pass form json to normal object #
      self.cart_id = json_result['id']