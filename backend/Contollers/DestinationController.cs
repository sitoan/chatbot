using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TourFlowBE.Models;

namespace TourFlowBE.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class DestinationController: ControllerBase
    {
        private readonly TourFlowContext _dbContext;
        public DestinationController(TourFlowContext dbContext)
        {
            _dbContext = dbContext;
        }
        
        //Get countries
        [HttpGet("countries")]
        public async Task<IActionResult> GetCountries()
        {
            var countries = await _dbContext.CountryDestinations.ToListAsync();
            return Ok(countries);
        }

        
        [HttpGet("{country}/cities")]
        public async Task<IActionResult> GetCities(string country)
        {
            var cities = await (from city in _dbContext.CityDestinations 
                                join countries in _dbContext.CountryDestinations
                                on city.CountryDestinationId equals countries.Id
                                where countries.Country == country
                                select new {
                                    city.Id,
                                    city.City
                                })
                                
                                .ToListAsync();
            return Ok(cities);
        }

        [HttpGet("city/{cityname}")]
        public async Task<IActionResult> GetCity(string cityname)
        {
            var city = await _dbContext.CityDestinations
                            .Select(c => new {
                                c.Id,
                                c.City
                            }).Where(c=>c.City == cityname)
                            .ToListAsync();
            return Ok(city);
        }
        //Get cities
        [HttpGet("cities")]
        public async Task<IActionResult> GetCities()
        {
            var cities = await _dbContext.CityDestinations
                            .Select(c => new {
                                c.Id,
                                c.City
                            })
                            .ToListAsync();
            return Ok(cities);
        }
 
 
    }
    
}