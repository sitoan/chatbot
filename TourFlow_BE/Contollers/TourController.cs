using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TourFlowBE.Models;
using TourFlowBE.ModelDtos;

namespace TourFlowBE.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class TourController: ControllerBase
    {
        private readonly TourFlowContext _dbContext; 
        public TourController(TourFlowContext dbContext)
        {
            _dbContext = dbContext; 
        }

        [HttpGet("test")]
        public IActionResult Get()
        {
            return Ok("hi");
        }
 

        // http://localhost:5175/api/tour?page=1&limit=10
        [HttpGet]
        public async Task<ActionResult> GetAllTours(int page = 1, int limit = 10)
        {
            if (page <= 0 || limit <= 0)
            {
                return BadRequest("page or limit must be greater than 0");
            }
            var tours = (from tour in _dbContext.Tours 
                        join cityDestination in _dbContext.CityDestinations 
                        on tour.CityDestinationId equals cityDestination.Id
                        join countryDestination in _dbContext.CountryDestinations
                        on cityDestination.CountryDestinationId equals countryDestination.Id 
                        select new {
                            tour.Id,
                            tour.DepartureLocation,
                            cityDestination.City,
                            countryDestination.Country,
                            tour.StartDate,
                            tour.EndDate,
                            Duration = tour.EndDate - tour.StartDate,
                            tour.Price,
                            tour.AvailableSlots, 
                            FirstImageUrl = _dbContext.Imgs
                                .Where(img => img.CityDestinationId == cityDestination.Id)
                                .Select(img => img.Url)
                                .FirstOrDefault() 
                        }).ToList(); 

            var totalItems = tours.Count;
            var totalPages = (int)Math.Ceiling(totalItems / (double)limit);
            var paginatedItems = tours.Skip((page - 1) * limit)
                                    .Take(limit);
            var response = new
                            {
                                data = paginatedItems,
                                currentPage = page,
                                totalPages = totalPages
                            };
            return Ok(response);
        }

        

        

   

        [HttpGet("destination/{destinationid}")]
        public async Task<IActionResult> GetToursByDestinationId(
                                                    int destinationid, int page = 1, int limit = 10)
        {
            if (page <= 0 || limit <= 0)
            {
                return BadRequest("page or limit must be greater than 0");
            }
            var tours = await (from tour in _dbContext.Tours 
                join cityDestination in _dbContext.CityDestinations 
                on tour.CityDestinationId equals cityDestination.Id
                join countryDestination in _dbContext.CountryDestinations
                on cityDestination.CountryDestinationId equals countryDestination.Id 
                where cityDestination.Id == destinationid
                select new {
                    tour.Id,
                    tour.DepartureLocation,
                    cityDestination.City,
                    countryDestination.Country,
                    tour.StartDate,
                    tour.EndDate,
                    Duration = tour.EndDate - tour.StartDate,
                    tour.Price,
                    tour.AvailableSlots, 
                    FirstImageUrl = _dbContext.Imgs
                        .Where(img => img.CityDestinationId == cityDestination.Id)
                        .Select(img => img.Url)
                        .FirstOrDefault() 
                }).ToListAsync();
                 var totalItems = tours.Count;
            var totalPages = (int)Math.Ceiling(totalItems / (double)limit);
            var paginatedItems = tours.Skip((page - 1) * limit)
                                    .Take(limit);
            var response = new
                            {
                                data = paginatedItems,
                                currentPage = page,
                                totalPages = totalPages
                            };
            return Ok(response); 
        }


        //url : http://localhost:5175/api/tour/getallforai
        [HttpGet("getallforai")]
        public async Task<IActionResult> GetAllAI()
        { 
            var tours = await (from tour in _dbContext.Tours 
                join cityDestination in _dbContext.CityDestinations 
                on tour.CityDestinationId equals cityDestination.Id
                join countryDestination in _dbContext.CountryDestinations
                on cityDestination.CountryDestinationId equals countryDestination.Id  
                select new {
                    tour.Id,
                    tour.DepartureLocation,
                    cityDestination.City,
                    countryDestination.Country,
                    tour.StartDate,
                    tour.EndDate,
                    Duration = tour.EndDate - tour.StartDate, 
                    tour.Price,
                    tour.AvailableSlots, 
                    FirstImageUrl = _dbContext.Imgs
                        .Where(img => img.CityDestinationId == cityDestination.Id)
                        .Select(img => img.Url)
                        .FirstOrDefault() 
                }).ToListAsync();

                var formattedTours = tours.Select(t => new {
                    t.Id,
                    t.DepartureLocation,
                    t.City,
                    t.Country,
                    StartDate = t.StartDate?.ToString("dd-MM-yyyy"),  
                    EndDate = t.EndDate?.ToString("dd-MM-yyyy"),
                    Duration = t.Duration?.Days+1,
                    t.Price,
                    t.AvailableSlots,
                    t.FirstImageUrl
                }).ToList(); 
            return Ok(formattedTours);
        }

        [HttpGet("{tourid}")]
        public async Task<IActionResult> GetTour(int tourid)
        { 
            var tour = await _dbContext.Tours
            .Where(t => t.Id == tourid)
            .Include(t => t.TourPlans)
            .Select(t => new
            {
                t.Id,
                t.DepartureLocation,
                t.CityDestination.City,
                t.StartDate,
                t.EndDate,
                Duration = (t.EndDate - t.StartDate).Value.Days + 1,
                t.Price,
                t.AvailableSlots,
                TourPlans = t.TourPlans.Select(tp =>  tp.Detail ).ToList()
            })
            .FirstOrDefaultAsync();
            if (tour != null)
            {
                return Ok(tour);
            } else {
                return NotFound();
            }

        }
        [HttpPost]
        [Authorize(Roles = "True")]
        public async Task<IActionResult> PostTour([FromBody]PostTourDto postTour)
        {
            try
            {
                var newTour = new Tour{
                    CityDestinationId =  postTour.CityDestinationId,
                    DepartureLocation = postTour.DepartureLocation,
                    StartDate = postTour.StartDate,
                    EndDate = postTour.EndDate,
                    Price = postTour.Price,
                    AvailableSlots = postTour.AvailableSlots,
                };
                await _dbContext.Tours.AddAsync(newTour);
                await _dbContext.SaveChangesAsync();
                var tourId = newTour.Id;

                var tourPlanController = new TourPlanController(_dbContext);
                await tourPlanController.Post(postTour.plans, tourId);
                await _dbContext.SaveChangesAsync();
                

                return Ok("Post successfully");

            } catch (Exception e){
                return BadRequest(e);
            }
        }
        
        [HttpPut("{tourId}")]
        [Authorize(Roles ="True")]
        public async Task<IActionResult> PutTour([FromBody]PutTourDto tourUpdate, int tourId)
        {
            var currentTour = await _dbContext.Tours.FindAsync(tourId);
            if (currentTour == null)
            {
                return NotFound("Error occur, can not find the tour");
            } else {
                if (tourUpdate.DepartureLocation != currentTour.DepartureLocation)
                {
                    currentTour.DepartureLocation = tourUpdate.DepartureLocation;
                }
                if (tourUpdate.StartDate != currentTour.StartDate)
                {
                    currentTour.StartDate = tourUpdate.StartDate;
                }
                if (tourUpdate.EndDate != currentTour.EndDate)
                {
                    currentTour.EndDate = tourUpdate.EndDate;
                }
                if (tourUpdate.Price != currentTour.Price)
                {
                    currentTour.Price = tourUpdate.Price;
                } 
                if (tourUpdate.AvailableSlots != currentTour.AvailableSlots)
                {
                    currentTour.AvailableSlots = tourUpdate.AvailableSlots;
                }
                var tourPlanController = new TourPlanController(_dbContext);
                await tourPlanController.Put(tourId, tourUpdate.plans);
                await tourPlanController.Post(tourUpdate.newPlans, tourId);
                await _dbContext.SaveChangesAsync();
                return Ok("Updated succesfully");

            }
        }   

        [HttpDelete("{tourId}")]
        [Authorize(Roles ="True")]
        public  async Task<IActionResult> Delete(int tourId)
        {
            var currentTour = await _dbContext.Tours.FindAsync(tourId);
            if (currentTour == null)
            {
                return NotFound();
            } else {
                 _dbContext.Tours.Remove(currentTour);
                 await _dbContext.SaveChangesAsync();
                 return Ok();
            }
        }
    }
}