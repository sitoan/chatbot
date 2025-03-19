using Microsoft.AspNetCore.Mvc; 
using TourFlowBE.Models;
using TourFlow_gitBE.ModelDtos;
using Microsoft.EntityFrameworkCore;
namespace TourFlow_gitBE.Contollers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TourOrderController : ControllerBase
    {
        private readonly TourFlowContext _dbContext;

        public TourOrderController(TourFlowContext dbContext)
        {
            _dbContext = dbContext;
        }

        [HttpGet]
        public IActionResult Get()
        {
            return Ok("hihi");
        }

        [HttpPost]
        public async Task<IActionResult> Post([FromBody]TourOrderDto order)
        { 
            if (order == null){
                return BadRequest("Order was null");
            } 
            if (order.Slots < 1) {
                return BadRequest("Slot < 1 ");
            }

            var tourOrder = new TourOrder{ 
                BookDate = DateTime.Now,
                TourflowUserId = order.TourflowUserId,
                TourBooked =  order.TourBooked, 
                Slots = order.Slots,
                TotalPrice = order.TotalPrice,
            };
            await _dbContext.TourOrders.AddAsync(tourOrder);
            await _dbContext.SaveChangesAsync();
            return Ok(tourOrder);

        }

        [HttpGet("{userId}")]
        public async Task<IActionResult> Get(int userId)
        {
            var query = await (from tourOrder in _dbContext.TourOrders
            join Tour in _dbContext.Tours
            on tourOrder.TourBooked equals Tour.Id
            where tourOrder.TourflowUserId == userId
            select new {
                Departure = Tour.DepartureLocation,
                TourName = Tour.CityDestination.City,
                BookDate = tourOrder.BookDate,
                Slots = tourOrder.Slots,
                Price = tourOrder.TotalPrice,
                Paid = tourOrder.Paid,
            }).ToListAsync();
            return Ok(query);    
        }

    }
}