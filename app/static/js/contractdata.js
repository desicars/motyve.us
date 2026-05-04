function get_el(el) {
  return document.getElementById(el);
}

document.addEventListener('DOMContentLoaded', () => {
  get_el('book').addEventListener('click', () => {
    if (get_el('policy').checked && get_el('reminders').checked && get_el('name').value.trim() && get_el('address').value.trim() && get_el('license').value.trim() && get_el('state').value.trim() && get_el('phone').value.trim()) {
      alert('Thank you!');
      get_el('content').innerHTML = '';
    } else {
      alert('Please fill all input fields and agree to the policy.');
    }
  });
});