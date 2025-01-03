using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TourFlowBE.Models;
using TourFlowBE.ModelDtos;

namespace TourFlowBE.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class ImgController: ControllerBase
    {
        private readonly TourFlowContext _dbContext;
        public ImgController(TourFlowContext dbContext)
        {
            _dbContext = dbContext;
        }

        [HttpGet("{TourId}")]
        public async Task<IActionResult> Get(int TourId)
        {
            var query =  from imgs in _dbContext.Imgs 
                            join tour in _dbContext.Tours
                            on imgs.CityDestinationId equals tour.CityDestinationId
                            where tour.Id == TourId
                            select imgs.Url;
                            
            return Ok(await query.ToListAsync());
        }
        [HttpPost]
        public async Task<IActionResult> Post(List<string> listImgs, int cityDestinationId)
        {
            try
            {
                listImgs.ForEach(async img => {
                   await _dbContext.Imgs.AddAsync(new Img{
                        CityDestinationId =  cityDestinationId,
                        Url = img,
                    });
                });
                // await _dbContext.SaveChangesAsync();
                return Ok("Add all images successfully");
            } catch (Exception e) {
                return BadRequest(e);
            }   
        }
    }

}