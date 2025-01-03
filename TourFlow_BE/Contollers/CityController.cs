using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TourFlowBE.Models;
using TourFlowBE.ModelDtos;

namespace TourFlowBE.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class CityController: ControllerBase
    {
        private readonly TourFlowContext _dbContext;
        public CityController( TourFlowContext dbContext)
        {
            _dbContext = dbContext;
        }
 

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var cities = await (from city in _dbContext.CityDestinations 
                                select new {
                                    city.Id,
                                    city.City
                                }).ToListAsync();
            return Ok(cities);
        }

        [HttpPost] 
        [Authorize(Roles = "True")]
        public async Task<IActionResult> Post([FromBody] CityDestinationDto city)
        {    
            try
            {
                var cityDestination = new CityDestination{
                        City =  city.City ,
                        CountryDestinationId = city.CountryDestinationId
                    };
                await _dbContext.CityDestinations.AddAsync(
                    cityDestination
                );
                await _dbContext.SaveChangesAsync(); 
                var cityDestinationId = cityDestination.Id;
                
                var imgController = new ImgController(_dbContext);
                await imgController.Post(city.listImgUrl, cityDestinationId);
                await _dbContext.SaveChangesAsync(); 
                
                
            } catch (Exception err) {
                return BadRequest("Exception: "+ err.Message);
            }
            return Ok();
        }

    }

    public class CityDestinationDto()
    {
        public string City { get; set; }
        public int? CountryDestinationId { get; set; }
        public List<string> listImgUrl { get; set; }
        
    }
}