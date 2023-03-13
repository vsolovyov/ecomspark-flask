This is a reimplementation of [EcomSpark](https://github.com/piranha/ecomspark)
in Python using Flask framework.

It's an example of a working eCommerce site: product list with endless scroll,
where you can add a product to a cart, etc.

It's built using [TwinSpark](https://piranha.github.io/twinspark-js/) on the
frontend, which allows you to add interactivity without writing a single line of
JavaScript.

App is written in a way when each endpoint is able to integrate with TwinSpark,
works with JS-less browsers and presents a JSON API (try `curl localhost:5000`).
