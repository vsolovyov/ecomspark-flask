from functools import wraps

from flask import Flask, request, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'something not really unique nor secret'


### "DB"
def make_product(product_id, in_cart):
    # hash(int) == int, convert to str to make it "random"
    product_hash = hash(str(product_id))
    return dict(
        id=product_id,
        price=product_hash % 90 + 10,
        pic=f'https://picsum.photos/seed/{product_hash}/240/300',
        in_cart=in_cart,
    )


### Handlers

@app.route('/')
def products_view():
    offset = request.args.get('offset', 0, type=int)
    cart = session.get('cart', [])
    next_offset = offset + 24
    products = [make_product(i, in_cart=i in cart)
                for i in range(offset, next_offset)]
    return ts_response(
        context=dict(
            offset=next_offset,
            products=products),
        partial='products-partial.html',
        full='index.html',
    )

@app.route('/cart')
def cart_view():
    cart = sorted(session.get('cart', []))
    products = [make_product(i, in_cart=True) for i in cart]
    return ts_response(
        context=dict(
            products=products,
            cart_size=len(cart)),
        partial='cart-partial.html',
        full='cart-page.html',
    )


@app.route('/cart/add', methods=['POST'])
def cart_add():
    product_id = request.form.get('id', type=int)
    if product_id is None:
        return "No id supplied", 400
    cart = [*session.get('cart', []), product_id]
    session['cart'] = cart
    return ts_response(
        context=dict(
            cart_size=len(cart),
            success=True),
        partial='cart-add.html',
        full=redirect(url_for('cart_view')),
    )


@app.route('/cart/remove', methods=['POST', 'DELETE'])
def cart_remove():
    product_id = request.form.get('id', type=int)
    if product_id is None:
        return "No id supplied", 400
    cart = session.get('cart', [])
    cart = [pid for pid in cart if pid != product_id]
    session['cart'] = cart
    return ts_response(
        context=dict(
            cart_size=len(cart),
            success=True),
        partial='cart-remove.html',
        full=redirect(url_for('cart_view')),
    )


### Twinspark support

def _accepts(content_type):
    accept = request.headers.get('accept')
    return accept and accept.startswith(content_type)


def ts_response(context, partial, full, status=200):
    if _accepts('text/html+partial'):
        return render_template(partial, **context)
    if _accepts('text/html') :
        if isinstance(full, str):
            return render_template(full, **context)
        return full
    return context
