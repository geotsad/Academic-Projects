<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        table {
            border-collapse: collapse;
            width: 30%;
            border: 1px solid black;
        }
        td, tr {
            width: 50%;
            padding: 8px;
            text-align: left;
        }
    </style>
</head>

<?php
// Ονοματεπώνυμο : Γεώργιος Τσαντίκης
// ΑΕΜ : 10722
// Email : tsangeor@ece.auth.gr


// Resume existing session (or start a new one)
session_start();

// If not logged in redirect to login page
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true || $_SESSION['username'] == '') {
    header("Location: login.php");
    exit;
}

$username = $_SESSION['username'];
$encryptionKey = isset($_SESSION['secret_key']) ? $_SESSION['secret_key'] : null;

// Συναρτήσεις Κρυπτογράφησης
function encryptData($data, $key) {
    $cipher = "aes-256-gcm";
    $ivlen = openssl_cipher_iv_length($cipher);
    $iv = openssl_random_pseudo_bytes($ivlen);
    $ciphertext = openssl_encrypt($data, $cipher, $key, OPENSSL_RAW_DATA, $iv, $tag);
    return base64_encode($iv . $tag . $ciphertext);
}

function decryptData($encryptedData, $key) {
    $cipher = "aes-256-gcm";
    $encryptedData = base64_decode($encryptedData);
    $ivlen = openssl_cipher_iv_length($cipher);
    $iv = substr($encryptedData, 0, $ivlen);
    $tag = substr($encryptedData, $ivlen, 16);
    $ciphertext = substr($encryptedData, $ivlen + 16);
    return openssl_decrypt($ciphertext, $cipher, $key, OPENSSL_RAW_DATA, $iv, $tag);
}

// Connect to the database
$conn=mysqli_connect("localhost","root","","pwd_mgr");
// Check connection
if (mysqli_connect_errno())	{ echo "Failed to connect: " . mysqli_connect_error(); exit(); }

// Check if 'Insert-new-website' button is selected
if(isset($_POST['new_website'], $_POST['new_username'], $_POST['new_password']) && 
   trim($_POST['new_website']) !='' && trim($_POST['new_username']) !='' && trim($_POST['new_password']) !='') {
	
	$new_website = trim($_POST['new_website']);
	$web_username = trim($_POST['new_username']);
	$web_password = trim($_POST['new_password']);

    // Κρυπτογράφηση
    if ($encryptionKey) {
        $encrypted_password = encryptData($web_password, $encryptionKey);
    } else {
        $encrypted_password = "KEY_ERROR"; 
    }

	$stmt = $conn->prepare("INSERT INTO websites (login_user_id, web_url, web_username, web_password) VALUES ((SELECT id FROM login_users WHERE username=?), ?, ?, ?)");
    $stmt->bind_param("ssss", $username, $new_website, $web_username, $encrypted_password);
	$stmt->execute();
    $stmt->close();

	unset($_POST['new_website']);
	unset($_POST['new_username']);
	unset($_POST['new_password']);
}

// Διαγραφή Site
if (isset($_POST['delete_website']) && isset($_POST['websiteid'])) {
    $stmt = $conn->prepare("DELETE FROM websites WHERE webid=? AND login_user_id=(SELECT id FROM login_users WHERE username=?)");
    $stmt->bind_param("is", $_POST['websiteid'], $username);
    $stmt->execute();
    $stmt->close();
}

// Εμφάνιση Sites
$stmt = $conn->prepare("SELECT * FROM websites WHERE login_user_id=(SELECT id FROM login_users WHERE username=?)");
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

echo "<h3>Entries of " . htmlspecialchars($username) . "</h3>";

if ($result->num_rows >= 1) {
	while ($row = $result -> fetch_assoc()) {
        // Αποκρυπτογράφηση
        $decrypted_pass = decryptData($row["web_password"], $encryptionKey);
        if ($decrypted_pass === false) $decrypted_pass = $row["web_password"] . " (Unencrypted)";

		echo "<table border=0>";
		echo	"<tr style='background-color: #f4f4f4;'><td colspan=2>" . htmlspecialchars($row["web_url"]) . "</td></tr>" . 
				"<tr><td>Username: " . htmlspecialchars($row["web_username"]) . "</td><td>Password: " . htmlspecialchars($decrypted_pass) . "</td></tr>";
		echo	"<tr><td><form method='POST' style='height: 3px'>" . 
				"<input type='hidden' name='websiteid' value='" . $row["webid"] . "'>" .
				"<button type='submit' name='delete_website'>Delete</button></form></td></tr>";
		echo	"<tr><td colspan=2 style=height: 20px;></td></tr>";
		echo "</table><p/>";
	}
} else {
	echo "<p><font color=red>No entries found.</font></p>";
}
$conn -> close();
?>

<body>
	<p/>
	<form method="POST" action="dashboard.php">
        <input type="text" name="new_website" placeholder="website"><br />
        <input type="text" name="new_username" placeholder="Username"><br />
        <input type="password" name="new_password" placeholder="Password"><br />
        <button type="submit">Insert new website</button>
    </form>
	<p/>
    <a href="notes.php">Notes - announcements</a>
	<p/>
    <a href="logout.php">Logout</a>
	<p/>
	<a href="index.html">Home page</a>
</body>
</html>