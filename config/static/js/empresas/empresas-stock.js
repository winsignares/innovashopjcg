document.addEventListener("DOMContentLoaded", function () {
  const fetchProducts = () => {
    axios
      .get("/producto/productos")
      .then((response) => {
        const products = response.data;
        if (products.length === 0) {
          renderNoProductsMessage();
        } else {
          renderProducts(products);
        }
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
      });
  };

  const fetchProveedores = () => {
    return axios
      .get("/proveedor/proveedores")
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.error("Error fetching proveedores:", error);
        return [];
      });
  };

  const fetchAllProducts = () => {
    return axios
      .get("/producto/all-products")
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.error("Error fetching all products:", error);
        return [];
      });
  };

  const renderNoProductsMessage = () => {
    const productContainer = document.getElementById("product-list");
    productContainer.innerHTML = "<p>No hay productos disponibles.</p>";
  };

  const renderProducts = (products) => {
    const productContainer = document.getElementById("product-list");
    productContainer.innerHTML = "";
    products.forEach((product) => {
      const productCard = document.createElement("div");
      productCard.classList.add("product-card");

      const productImage = document.createElement("img");
      productImage.src = product.img_src;
      productCard.appendChild(productImage);

      const productInfo = document.createElement("div");
      productInfo.classList.add("product-info");

      const productName = document.createElement("div");
      productName.classList.add("product-name");
      productName.textContent = product.nombre;
      productInfo.appendChild(productName);

      const productPrice = document.createElement("div");
      productPrice.classList.add("product-price");
      productPrice.textContent = `Precio: $${product.precio}`;
      productInfo.appendChild(productPrice);

      const btnContainer = document.createElement("div");
      btnContainer.classList.add("btn-container");

      const editButton = document.createElement("button");
      editButton.classList.add("btn", "btn-primary");
      editButton.textContent = "Editar";
      editButton.addEventListener("click", () => openEditModal(product));
      btnContainer.appendChild(editButton);

      const deleteButton = document.createElement("button");
      deleteButton.classList.add("btn", "btn-danger");
      deleteButton.textContent = "Eliminar";
      deleteButton.addEventListener("click", () => deleteProduct(product.id));
      btnContainer.appendChild(deleteButton);

      productInfo.appendChild(btnContainer);
      productCard.appendChild(productInfo);
      productContainer.appendChild(productCard);
    });
  };

  const openEditModal = (product) => {
    Promise.all([fetchProveedores(), fetchAllProducts()]).then(
      ([proveedores, allProducts]) => {
        const proveedorSelect = document.getElementById("proveedor_id");
        proveedorSelect.innerHTML = "<option value=''>Seleccionar</option>";
        proveedores.forEach((proveedor) => {
          const option = document.createElement("option");
          option.value = proveedor.id;
          option.textContent = proveedor.nombre;
          if (proveedor.id === product.proveedor_id) {
            option.selected = true;
          }
          proveedorSelect.appendChild(option);
        });

        const productoAlternoSelect = document.getElementById("producto_alterno_id");
        productoAlternoSelect.innerHTML = "<option value=''>Seleccionar</option>";
        if (allProducts.length === 0) {
          const noProductsOption = document.createElement("option");
          noProductsOption.value = "";
          noProductsOption.textContent = "No hay ningun producto para ser alterno en este momento";
          productoAlternoSelect.appendChild(noProductsOption);
        } else {
          allProducts.forEach((prod) => {
            const option = document.createElement("option");
            option.value = prod.id;
            option.textContent = prod.nombre;
            if (prod.id === product.producto_alterno_id) {
              option.selected = true;
            }
            productoAlternoSelect.appendChild(option);
          });
        }

        const modal = new bootstrap.Modal(document.getElementById("addStockModal"));
        document.getElementById("addStockModalLabel").textContent = "Editar Producto";
        document.getElementById("nombre").value = product.nombre;
        document.getElementById("descripcion").value = product.descripcion;
        document.getElementById("precio").value = product.precio;
        document.getElementById("existencias").value = product.existencias;
        document.getElementById("min_existencias").value = product.min_existencias;
        document.getElementById("img_src").required = false; // Image is optional for editing
        document.getElementById("add-stock-form").dataset.editing = product.id;
        modal.show();
      }
    );
  };

  const deleteProduct = (productId) => {
    axios
      .delete(`/producto/delete/${productId}`)
      .then((response) => {
        alert("Producto eliminado con éxito.");
        fetchProducts();
      })
      .catch((error) => {
        console.error("Error eliminando el producto:", error);
        alert("Hubo un error al eliminar el producto.");
      });
  };

  document
    .getElementById("add-stock-form")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(this);
      const isEditing = this.dataset.editing;

      if (isEditing) {
        axios
          .put(`/producto/edit/${isEditing}`, formData)
          .then((response) => {
            alert("Producto editado con éxito.");
            fetchProducts();
          })
          .catch((error) => {
            console.error("Error editando el producto:", error);
            alert("Hubo un error al editar el producto.");
          });
      } else {
        axios
          .post("/producto/add-stock", formData)
          .then((response) => {
            alert("Producto añadido con éxito.");
            fetchProducts();
          })
          .catch((error) => {
            console.error("Error añadiendo el producto:", error);
            alert("Hubo un error al añadir el producto.");
          });
      }
    });

  // Fetch and populate proveedor and producto_alterno options when the page loads
  Promise.all([fetchProveedores(), fetchAllProducts()]).then(
    ([proveedores, allProducts]) => {
      const proveedorSelect = document.getElementById("proveedor_id");
      proveedorSelect.innerHTML = "<option value=''>Seleccionar</option>";
      proveedores.forEach((proveedor) => {
        const option = document.createElement("option");
        option.value = proveedor.id;
        option.textContent = proveedor.nombre;
        proveedorSelect.appendChild(option);
      });

      const productoAlternoSelect = document.getElementById("producto_alterno_id");
      productoAlternoSelect.innerHTML = "<option value=''>Seleccionar</option>";
      if (allProducts.length === 0) {
        const noProductsOption = document.createElement("option");
        noProductsOption.value = "";
        noProductsOption.textContent = "No hay ningun producto para ser alterno en este momento";
        productoAlternoSelect.appendChild(noProductsOption);
      } else {
        allProducts.forEach((product) => {
          const option = document.createElement("option");
          option.value = product.id;
          option.textContent = product.nombre;
          productoAlternoSelect.appendChild(option);
        });
      }
    }
  );

  // Add Cotizar functionality
  document.getElementById('cotizar-button').addEventListener('click', function() {
    const formData = new FormData(document.getElementById('add-stock-form'));
    const proveedorId = formData.get('proveedor_id');
    const productId = formData.get('producto_alterno_id');
    const precio = parseFloat(formData.get('precio'));
    const cantidad = parseInt(formData.get('existencias'));

    if (!proveedorId || !precio || !cantidad) {
      alert("Por favor, complete todos los campos necesarios para la cotización.");
      return;
    }

    const totalPrecio = precio * cantidad;

    const cotizacionData = {
      proveedor_id: proveedorId,
      producto_id: productId || null,  // Producto alterno can be nullable
      cantidad: cantidad,
      precio_total: totalPrecio
    };

    console.log("Sending cotizacion data:", cotizacionData);  // Debugging statement

    axios.post('/empresa/cotizar', cotizacionData)
    .then(function(response) {
      alert("Cotización realizada con éxito. Total: $" + totalPrecio);
      // Optionally, redirect to a different page or update the UI
    })
    .catch(function(error) {
      console.error("Error realizando la cotización:", error);
      alert("Hubo un error al realizar la cotización.");
    });
});

  fetchProducts();
});
