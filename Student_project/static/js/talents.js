// document.addEventListener('DOMContentLoaded', function () {
//     document.querySelectorAll('.skill-card').forEach(card => {
//         card.addEventListener('click', function () {
//             const skillId = this.getAttribute('data-skill-id');
//             fetch(`talents/${skillId}/`)
//                 .then(response => response.json())
//                 .then(data => {
//                     document.querySelector('.section-heading').textContent = `Specialized ${data.random_skill} experts you can count on`;
//                     document.querySelector('.stat:nth-child(2) h3').textContent = data.random_contracts + ' contracts';
//                     document.querySelector('.stat:nth-child(2) p').textContent = `Involving ${data.random_skill} work in the past year.`;

//                     const servicesContainer = document.getElementById('services-container');
//                     servicesContainer.innerHTML = '';

//                     data.related_services.forEach(service => {
//                         const serviceCard = document.createElement('div');
//                         serviceCard.classList.add('col-12', 'col-sm-6', 'col-lg-3', 'mb-4', 'd-flex', 'justify-content-center');
//                         serviceCard.innerHTML = `
//                             <div class="card card-custom h-100">
//                                 <div class="card-body">
//                                     <h5 class="card-title">${service.name}</h5>
//                                     <div class="rating">${service.rating}</div>
//                                     <div class="profile-pics">
//                                         ${data.related_user_profiles.map(user => `<img src="${user.profile_image}" alt="${user.username}">`).join('')}
//                                     </div>
//                                 </div>
//                             </div>`;
//                         servicesContainer.appendChild(serviceCard);
//                     });
//                 });
//         });
//     });
// });