<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Build Your Custom Shop Template</title>
<style>
    body {
      font-family: Arial, sans-serif;
      background-color: #eaf2fb;
      margin: 0;
      padding: 0;
    }
    .container {
      background: white;
      max-width: 800px;
      margin: 40px auto;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    h2 {
      color: #2c3e50;
    }
    h3 {
      color: #2c3e50;
    }
    .section {
      margin-bottom: 30px;
    }
    .instructions {
      margin: 10px 0;
      font-weight: bold;
    }
    .question {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      margin-bottom: 8px;
    }
    .question input[type="checkbox"] {
      margin-top: 4px;
      flex-shrink: 0;
    }
    .question label {
      display: inline-block;
      max-width: 90%;
      line-height: 1.4;
    }
    .custom-question-inputs {
      margin-top: 10px;
    }
    button {
      display: block;
      width: 100%;
      background-color: #4a90e2;
      color: white;
      padding: 12px;
      border: none;
      font-size: 16px;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 30px;
    }
    button:hover {
      background-color: #357ab8;
    }
    .recommended-btn {
      background-color: #27ae60;
      margin-bottom: 20px;
    }
    .add-btn {
      background-color: #ecf0f1;
      color: #2c3e50;
      font-weight: bold;
      border: 1px solid #bdc3c7;
      width: auto;
      margin-top: 10px;
      padding: 6px 10px;
      border-radius: 6px;
    }
  </style>
</head>
<body>
<div class="container">
<h2>Build Your Custom Shop Template</h2>

<p>Use this form to create a shop template. Required sections are preselected. You may also add your own custom questions in each section.<br/>
    The shopper will be required to describe and summarize their experience after each section.</p>
<form id="shopForm"><div style="margin-bottom: 20px;">
<label style="font-weight: bold; background-color: #27ae60; color: white; padding: 12px 20px; border-radius: 8px; display: inline-block; cursor: pointer; font-size: 16px;">
<input id="recommendedToggle" style="margin-right: 10px; transform: scale(1.5);" type="checkbox"/>
  Use Recommended Template
</label>
</div>
<div class="section">
<h3>Agent &amp; Visit Information</h3>
<div class="instructions">Select which details you want to include:</div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Agent Phoned</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Date of Call</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Time of Call</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Length of Call</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Other Calls</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Agent Shopped</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Date of Visit</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Time of Visit</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Length of Visit</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Weather Conditions</label></div>
<button class="add-btn" onclick="addCustomQuestion('custom_agent')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_agent"></div>
</div>
<div class="section">
<h3>Shopper Information</h3>
<div class="instructions">Select the fields to include:</div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Shopper Name</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Name Given (Telephone)</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Name Given (On-Site)</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Guest Accompanying Shopper</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Relationship to Shopper</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Address</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>City</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>State</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Zip</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Telephone</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Email Address</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Traffic Source</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Apartment Size</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Date Needed</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Pets</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Number of Occupants</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Reason for Moving</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Specific Apartment Needs</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Specific Property Preferences</label></div>
<div class="question"><input checked="" disabled="" type="checkbox"/><label>Ideal Living Environment</label></div>
<button class="add-btn" onclick="addCustomQuestion('custom_shopper')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_shopper"></div>
</div>
<div class="section">
<h3>Executive Summary</h3>
<div class="question"><input type="checkbox"/><label>Overall Attitude and Impression</label></div>
<div class="question"><input type="checkbox"/><label>Strengths of the Associate's Presentation</label></div>
<div class="question"><input type="checkbox"/><label>Opportunities to Improve</label></div>
<div class="question"><input type="checkbox"/><label>Overall Summary of Experience</label></div>
<button class="add-btn" onclick="addCustomQuestion('custom_exec')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_exec"></div>
</div>
<div class="section">
<h3>Telephone – First Impression</h3>
<div class="question"><input type="checkbox"/><label>Number of Calls Made Before Reaching a Live Person</label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate answer the phone with the name of the property and identify their self?</label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate obtain your name within the first 30 seconds of the telephone call and effectively use it during the conversation?</label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate convey a sincere and friendly attitude and appear genuinely interested in serving you?</label></div>
<button class="add-btn" onclick="addCustomQuestion('custom_phone1')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_phone1"></div>
</div>
<div class="section">
<h3>Telephone – Connect With Customer</h3>
<div class="question"><input type="checkbox"/><label>Asked open-ended questions?</label></div>
<div class="question"><input type="checkbox"/><label>Asked at least 3 qualifying items?</label></div>
<div class="question"><input type="checkbox"/><label>Used positive phrasing?</label></div>
<div class="question"><input type="checkbox"/><label>Built rapport and conversation?</label></div>
<div class="question"><input type="checkbox"/><label>Did the associate ask at least three of the items below, in a conversational manner? (i.e. did not just ask a list of questions or bullet point the questions.)</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Size apartment</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Move-in date</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Lease term</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Floor level preference</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>View preference</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Number of occupants</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Animals</label></div>
<div class="question"><input type="checkbox"/><label>Used active listening to match apartment features with customer needs</label></div>
<div class="question"><input type="checkbox"/><label>Used property website or virtual materials as a selling tool</label></div>
<div class="question"><input type="checkbox"/><label>Asked for contact information</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Phone</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Email</label>
</div>
<button class="add-btn" onclick="addCustomQuestion('custom_phone2')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_phone2"></div>
<h3>Property Visit</h3>
<div class="question"><input type="checkbox"/><label>Property signage and directions visible?</label></div>
<div class="question"><input type="checkbox"/><label>Amenities and grounds clean?</label></div>
<div class="question"><input type="checkbox"/><label>Leasing office professional and clean?</label></div>
<div class="question"><input type="checkbox"/><label>Were the main property signs clear, visible and in good condition?</label></div>
<div class="question"><input type="checkbox"/><label>Did you easily locate the leasing office/information center?</label></div>
<div class="question"><input type="checkbox"/><label>Were the lawns and landscaping neat and trim, and free of all trash?</label></div>
<div class="question"><input type="checkbox"/><label>Was the general appearance of the parking area in good condition and free of trash?</label></div>
<div class="question"><input type="checkbox"/><label>Were the property amenities you saw (i.e. pool, tennis courts, etc.) clean, attractive, and well maintained?</label></div>
<div class="question"><input type="checkbox"/><label>Was the leasing office (including desks) clean, neat, and orderly?</label></div>
<div class="question"><input type="checkbox"/><label>Was your first impression of the property and curb appeal a positive one?</label></div>
<button class="add-btn" onclick="addCustomQuestion(\'custom_visit\')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_visit"></div>
</div>
<div class="section">
<h3>Positive First Impression</h3>
<div class="question"><input type="checkbox"/><label>Did the Associate make a positive first impression and appear genuinely interested in serving you?</label></div><div class="section">
<div class="question"><input type="checkbox"/><label>Did the Associate deliver a professional greeting by doing any of the following:</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Stand</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Smile</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Introduce Themselves</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Offer Welcome handshake/high five</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Offer refreshment before the tour</label></div>
<div class="question"><input type="checkbox"/><label>Was the Associate prepared for your visit (if you called first) to make you feel welcomed by doing the following:</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Knew you were showing up</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Had relevant information available (e.g. price sheet, layouts, map, etc.)</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Greet you by name</label></div>
<button class="add-btn" onclick="addCustomQuestion('tour_first_impression')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="tour_first_impression"></div>
<h3>Tour – Connect with Customers</h3>
<div class="question"><input type="checkbox"/><label>Asked or recapped preferences to match needs (e.g. "I remember you mentioned...")</label></div>
<div class="question"><input type="checkbox"/><label>Use active listening techniques?</label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate use positive phrasing throughout the conversation?</label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate ask questions to generate conversation and connection? </label></div>
<button class="add-btn" onclick="addCustomQuestion('tour_connect_with_customers')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="tour_connect_with_customers"></div>
</div>
<h3>Tour – Present the Property</h3>
<div class="question"><input type="checkbox"/><label>Did the Associate lead the tour/presentation with confidence and excitement, while inviting you to ask questions along the way?</label></div>
<div class="question"><input type="checkbox"/><label>Did the associate take a set tour path and highlight property amenities including customer service areas (e.g., maintenance services, resident events, awards property/associate has received etc.)?</label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate show an apartment that was tour ready (i.e. clean, made-ready, lights on)? </label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate mention benefits for the apartment features demonstrated (e.g. sell the features of the home and property that the customer said was important to them)?</label></div>
<div class="question"><input type="checkbox"/><label>Did the Associate discuss any of the following neighboring conveniences?</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Shopping</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Recreational Facilities (e.g. park, tennis court, basketball, etc)</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Dining</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Transportation</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Entertainment</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Nearby hospitals/Doctors offices</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Animal facilities (e.g. vet, dog park, etc.)</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Grocery Stores</label></div>
<button class="add-btn" onclick="addCustomQuestion('tour_present_the_property')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="tour_present_the_property"></div>
</div>
<div class="section">
<h3>Follow-Up</h3>
<div class="question"><input type="checkbox"/><label>Follow up within 48 hours?</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Phone Call</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Email</label></div>
<div class="question" style="margin-left: 20px;"><input type="checkbox"/><label>Text</label></div>
<div class="question"><input type="checkbox"/><label>Asked to apply/reserve a unit?</label></div>
<button class="add-btn" onclick="addCustomQuestion('custom_follow')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_follow"></div>
</div>
<div class="section">
<h3>Fair Housing &amp; Safety</h3>
<div class="question"><input type="checkbox"/><label>Avoided discriminatory comments?</label></div>
<div class="question"><input type="checkbox"/><label>Avoided security/safety language?</label></div>
<button class="add-btn" onclick="addCustomQuestion('custom_fair')" type="button">+ Add Custom Question</button>
<div class="custom-question-inputs" id="custom_fair"></div>
</div>
<button type="submit">Save Template</button>
</form>
</div>
</body>
</html>
<script>
let isRecommendedTemplate = false;

document.getElementById("recommendedToggle").addEventListener("change", function () {
  isRecommendedTemplate = this.checked;
  if (this.checked) {
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true);
  }
});

document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
  cb.addEventListener("change", function () {
    if (isRecommendedTemplate && !this.checked) {
      document.getElementById("recommendedToggle").checked = false;
      isRecommendedTemplate = false;
    }
  });
});

document.querySelectorAll('button.add-btn').forEach(btn => {
  btn.addEventListener("click", function () {
    if (isRecommendedTemplate) {
      document.getElementById("recommendedToggle").checked = false;
      isRecommendedTemplate = false;
    }
  });
});

document.getElementById('shopForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const sections = document.querySelectorAll('.section');
  const template = {};

  sections.forEach(section => {
    const title = section.querySelector('h3')?.textContent || '';
    const questions = [];

    section.querySelectorAll('input[type="checkbox"]:checked').forEach(cb => {
      if (cb.nextElementSibling) {
        questions.push(cb.nextElementSibling.textContent.trim());
      }
    });

    section.querySelectorAll('input[name="custom"]').forEach(input => {
      if (input.value.trim()) {
        questions.push(input.value.trim());
      }
    });

    if (questions.length > 0) {
      template[title] = questions;
    }
  });

  try {
    const res = await fetch('/save-template', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ template, recommended: isRecommendedTemplate })
    });

    const result = await res.json();
    if (res.status === 201) {
      alert(result.message);
      window.location.href = "/dashboard";
    } else {
      alert(result.error || "Unexpected error occurred.");
    }
  } catch (err) {
    console.error("Error:", err);
    alert("Template failed due to server error.");
  }
});
</script>

