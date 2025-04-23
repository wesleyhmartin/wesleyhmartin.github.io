<?php
// Ensure we send the right content type to Twilio
header("Content-Type: application/xml");

// Output the actual TwiML XML
echo '<?xml version="1.0" encoding="UTF-8"?>';
?>
<Response>
    <Play>https://wesleymartin.net/media/hotline.mp3</Play>
</Response>