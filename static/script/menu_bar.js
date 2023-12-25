window.application = window.application || {};

//navigation function that can be called from any page
window.application.goToTargetView = function(event) {
  if (event && event.preventDefault) {
    event.preventDefault();
  }

  var targetId = event.target.id || event.currentTarget.id;
  var targetUrl = '';


  switch (targetId) {
    case 'Asthma_Information':
    case 'Asthma_Information_':
    case 'Asthma_Information_ba':
    case 'Asthma_Information_bc':
    case 'Asthma_Information_bg':
    case 'Asthma_Information_bk':
      targetUrl = 'Asthma_Info.html';
      break;
    case 'London_Air_Quality_Info':
      targetUrl = 'Air_Quality_Map.html';
      break;
    case 'Group_bc':
      targetUrl = 'Air_Quality_Stats.html';
      break;
    case 'FAQ':
      targetUrl = 'FAQPage.html';
      break;
    case 'Learn_More':
      targetUrl = 'Asthma_Info.html';
      break;
    case 'Home':
      targetUrl = 'Home__1.html';
      break;
    default:
      console.error('No target URL defined for element ID:', targetId);
      return;
  }

  window.location.href = targetUrl;
};
document.addEventListener('DOMContentLoaded', () => {
    // Define the CSS selectors for each menu item
    var menuSelectors = ['#Asthma_Information', '#London_Air_Quality_Info', '#Air_Quality_Statistics', '#FAQ', '#Learn_More', '#Home'];
    
    menuSelectors.forEach(function(selector) {
      var element = document.querySelector(selector);
      if (element) {
        element.addEventListener('click', window.application.goToTargetView);
      }
    });
  });