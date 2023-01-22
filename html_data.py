HTML_DATA="""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>CyberSpace - FileSearch</title>
  <meta content="Index page" name="description">
  <!-- Favicons -->
  <link href="https://raw.githubusercontent.com/sachinOraon/media-server-suite/master/volumes/home-page/assets/img/favicon.png" rel="icon">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">
  <!-- Vendor CSS Files -->
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/animate.css/animate.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/aos/aos.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/glightbox/css/glightbox.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/remixicon/remixicon.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/swiper/swiper-bundle.min.css" rel="stylesheet">
  <!-- Template Main CSS File -->
  <link href="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/css/style.css" rel="stylesheet">
</head>
<body>
  <!-- ======= Header ======= -->
  <header id="header" class="fixed-top d-flex align-items-center  header-transparent ">
    <div class="container d-flex align-items-center justify-content-between">
      <div class="logo">
        <h1><a href="https://gdrive.movies-mca.workers.dev" target="_blank">CyberSpace Cloud ☁</a></h1>
      </div>
    </div>
  </header><!-- End Header -->
  <!-- ======= Hero Section ======= -->
  <section id="hero" class="d-flex flex-column justify-content-end align-items-center">
    <div id="heroCarousel" data-bs-interval="5000" class="container carousel carousel-fade" data-bs-ride="carousel">
      <!-- Slide 1 -->
      <div class="carousel-item active">
        <div class="carousel-container">
          <h2 class="animate__animated animate__fadeInDown">GDrive Search Bot™</h2>
          <p class="animate__animated fanimate__adeInUp">Welcome to the results page for the query <mark>{search_query}</mark> This page was created by a <strong><a href="https://t.me/Mirror2GdriveBot">Telegram</a></strong> bot. You can use this bot to search files stored in GDrives. Please join our Telegram group for more details and scroll down to see the results.</p>
          <a href="https://t.me/+xAIvM07WT1s4MWI1" class="btn-get-started animate__animated animate__fadeInUp scrollto">Join Group</a>
        </div>
      </div>
    </div>
    <svg class="hero-waves" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 24 150 28 " preserveAspectRatio="none">
      <defs>
        <path id="wave-path" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z">
      </defs>
      <g class="wave1">
        <use xlink:href="#wave-path" x="50" y="3" fill="rgba(255,255,255, .1)">
      </g>
      <g class="wave2">
        <use xlink:href="#wave-path" x="50" y="0" fill="rgba(255,255,255, .2)">
      </g>
      <g class="wave3">
        <use xlink:href="#wave-path" x="50" y="9" fill="#fff">
      </g>
    </svg>
  </section><!-- End Hero -->
  <main id="main">
    <!-- ======= Services Section ======= -->
    <section id="results" class="services">
      <div class="container">
        <div class="section-title" data-aos="zoom-out">
          <h2>Files Found: <strong>{search_count}</strong></h2>
          <p>{search_query}</p>
        </div>
        <div class="row">{search_results}</div>
      </div>
    </section><!-- End Services Section -->
  </main><!-- End #main -->
  <!-- ======= Footer ======= -->
  <footer id="footer">
    <div class="container">
      <h3>GDrive File Searching Bot</h3>
      <p>Search and download the files stored in multiple shared drives.</p>
      <div class="social-links">
        <a href="https://github.com/lokesh-go/google-services" target="_blank"><i class="bx bxl-github"></i></a>
        <a href="https://t.me/Mirror2GdriveBot" target="_blank"><i class="bx bxl-telegram"></i></a>
        <a href="https://t.me/+xAIvM07WT1s4MWI1" target="_blank"><i class='bx bx-cloud-download'></i></a>
        <a href="https://www.linkedin.com/in/lokesh-chandra-46ba3b15a/" target="_blank"><i class='bx bxl-linkedin-square'></i></a>
      </div>
      <div class="copyright">
        &copy; Copyright <strong><span>CyberSpace™</span></strong>. All Rights Reserved
      </div>
      <div class="credits">
        Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>
      </div>
    </div>
  </footer><!-- End Footer -->
  <a href="#results" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>
  <!-- Vendor JS Files -->
  <script src="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/aos/aos.js"></script>
  <script src="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/glightbox/js/glightbox.min.js"></script>
  <script src="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/isotope-layout/isotope.pkgd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/vendor/swiper/swiper-bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js" crossorigin="anonymous"></script>
  <!-- Template Main JS File -->
  <script src="https://cdn.jsdelivr.net/gh/sachinOraon/media-server-suite@master/volumes/home-page/assets/js/main.js"></script>
  <script>$(document).ready(function(){$("html, body").animate({ scrollTop: $('#results').offset().top }, 1000);});</script>
</body>
</html>
"""
