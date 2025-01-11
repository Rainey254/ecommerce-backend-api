document.addEventListener("DOMContentLoaded", () => {
    // Handle 'Remove from Wishlist' button clicks
    const wishlistButtons = document.querySelectorAll(".remove-wishlist");
  
    wishlistButtons.forEach(button => {
      button.addEventListener("click", (event) => {
        const productId = event.target.dataset.productId;
  
        // Send a DELETE request to remove the product from the wishlist
        fetch(`/wishlist/${productId}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Remove the item from the DOM
            const listItem = event.target.closest("li");
            listItem.remove();
  
            // Display a success message
            alert("Item successfully removed from your wishlist.");
          } else {
            alert("Failed to remove item. Please try again.");
          }
        })
        .catch(error => {
          console.error("Error:", error);
          alert("An error occurred. Please try again later.");
        });
      });
    });
  
    // Handle profile updates
    const profileForm = document.querySelector("#profile-form");
    if (profileForm) {
      profileForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission
  
        const formData = new FormData(profileForm);
  
        // Send a POST request to update the profile
        fetch("/update-profile", {
          method: "POST",
          body: JSON.stringify(Object.fromEntries(formData)),
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert("Profile updated successfully.");
            // Optionally refresh the page or update the UI dynamically
          } else {
            alert("Failed to update profile. Please try again.");
          }
        })
        .catch(error => {
          console.error("Error:", error);
          alert("An error occurred. Please try again later.");
        });
      });
    }
  
    // Fetch and update order history dynamically
    const orderHistorySection = document.querySelector("#order-history");
    if (orderHistorySection) {
      fetch("/order-history")
        .then(response => response.json())
        .then(data => {
          if (data.orders && data.orders.length > 0) {
            const orderList = document.createElement("ul");
  
            data.orders.forEach(order => {
              const listItem = document.createElement("li");
              listItem.innerHTML = `
                <p><strong>Order ID:</strong> ${order.id}</p>
                <p><strong>Date:</strong> ${order.date}</p>
                <p><strong>Total:</strong> ${order.total}</p>
              `;
              orderList.appendChild(listItem);
            });
  
            // Replace existing order history content with the updated list
            orderHistorySection.innerHTML = "<h3>Order History</h3>";
            orderHistorySection.appendChild(orderList);
          } else {
            orderHistorySection.innerHTML = `
              <h3>Order History</h3>
              <p>You have no order history.</p>
            `;
          }
        })
        .catch(error => {
          console.error("Error fetching order history:", error);
        });
    }
  });  