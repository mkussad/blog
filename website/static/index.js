// Function to handle liking/unliking a post
function like(postId) {
  // Get elements by their IDs
  const likeCount = document.getElementById(`likes-count-${postId}`);
  const likeButton = document.getElementById(`like-button-${postId}`);

  // Make a POST request to the server to like/unlike the post
  fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json()) // Parse the response as JSON
    .then((data) => {
      // Update the like count displayed on the page
      likeCount.innerHTML = data["likes"];

      // Update the like button icon based on whether the user liked the post
      if (data["liked"] === true) {
        likeButton.className = "fas fa-thumbs-up"; // User liked the post
      } else {
        likeButton.className = "far fa-thumbs-up"; // User unliked the post
      }
    })
    .catch((e) => alert("Could not like post.")); // Handle errors
}