using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TourFlowBE.Models;

namespace TourFlowBE.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class CountryController: ControllerBase
    {
        private readonly TourFlowContext _dbContext;
        public CountryController( TourFlowContext dbContext)
        {
            _dbContext = dbContext;
        }

        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var countries = await _dbContext.CountryDestinations
                            .Select(c => new {
                                c.Id,
                                c.Country
                            }).ToListAsync();
            return Ok(countries);
        }

        [HttpPost] 
        [Authorize(Roles = "True")]
        public async Task<IActionResult> Post([FromBody] CountryDestinationDto country)
        {   
            try
            {
                await _dbContext.CountryDestinations.AddAsync(
                    new CountryDestination{
                        Country =  country.Country
                    }
                );
                await _dbContext.SaveChangesAsync();
            } catch (Exception err) {
                return BadRequest("Exception: "+ err.Message);
            }
            return Ok();
        }

    }

    public class CountryDestinationDto()
    {
        public string Country { get; set; }
    }
}