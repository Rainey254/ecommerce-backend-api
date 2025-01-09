// Ensure the DOM is fully loaded before running scripts
document.addEventListener("DOMContentLoaded", () => {
    // Handle 'Remove from Wishlist' button clicks
    const wishlistButtons = document.querySelectorAll(".remove-wishlist");
    
    wishlistButtons.forEach(button => {
      button.addEventListener("click", (event) => {
        const productId = event.target.dataset.productId;
  
        // Confirm before removing the product
        const confirmRemoval = confirm("Are you sure you want to remove this item from your wishlist?");
        if (confirmRemoval) {
          // Send a DELETE request to the server to remove the product
          fetch(`/wishlist/${productId}`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then(response => {
            if (response.ok) {
              // Remove the item from the DOM if the request is successful
              event.target.parentElement.remove();
              alert("Item removed from your wishlist.");
            } else {
              alert("Failed to remove item from your wishlist. Please try again.");
            }
          })
          .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again later.");
          });
        }
      });
    });
  });  