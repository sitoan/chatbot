using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TourFlowBE.ModelDtos;
using TourFlowBE.Models;

namespace TourFlowBE.Controller
{
    [ApiController]
    [Route("api/[controller]")]

    public class TourPlanController: ControllerBase
    {
        private readonly TourFlowContext _dbContext;
        public TourPlanController(TourFlowContext dbContext)
        {
            _dbContext = dbContext;
        }

        // GET http://localhost:5175/api/tourplan/<tourId>
        
        [HttpGet("{TourId}")]
        public async Task<IActionResult> Get(int TourId)
        {
            var query = from tourplan in _dbContext.TourPlans
                        where tourplan.TourId == TourId
                        select new {
                            detailPlan = tourplan.Detail
                        };
            return Ok(await query.ToListAsync());
        }
        [HttpGet("withId/{TourId}")]
        public async Task<IActionResult> GetWithIdInResponse(int TourId)
        {
            var query = from tourplan in _dbContext.TourPlans
                        where tourplan.TourId == TourId
                        select new {
                            id =  tourplan.Id,
                            detailPlan = tourplan.Detail
                        };
            return Ok(await query.ToListAsync());
        }

        [HttpPost]
        public async Task<IActionResult> Post(List<string> plans, int tourId)
        {
            try 
            {
                plans.ForEach(async plan => {
                   await _dbContext.TourPlans.AddAsync(new TourPlan{
                        TourId = tourId,
                        Detail = plan,
                    });
                });
                // await _dbContext.SaveChangesAsync();
                return Ok("Add all images successfully");
            } catch(Exception e) {
                return BadRequest(e.Message);
            }
        }

       [HttpPut("{tourId}")]
       public async Task<IActionResult> Put(int tourId, List<UpdatePlanDto> plans)
       {
            var originalPlans = await _dbContext.TourPlans
            .Where(tp => tp.TourId == tourId)
            .ToListAsync();

            List<int> originalPlanIds = new List<int> ();
            List<int> planIds = new List<int> ();

            foreach (var plan in plans) {
                planIds.Add (plan.Id);
            }
            foreach (var plan in originalPlans) {
                originalPlanIds.Add (plan.Id);
            }
            List<int> deletedPlans = new List<int>();
            if (originalPlanIds != planIds) {
                deletedPlans = originalPlanIds.Except (planIds).ToList();
            } 
            foreach(var deletedPlan in deletedPlans) {
                Console.WriteLine(deletedPlan);
                var tourPlan = await _dbContext.TourPlans.FindAsync(deletedPlan);
                _dbContext.TourPlans.Remove(tourPlan);
            }
            await _dbContext.SaveChangesAsync();

            originalPlans = await _dbContext.TourPlans
            .Where(tp => tp.TourId == tourId)
            .ToListAsync(); 

            for (int i = 0;  i < plans.Count; i++)
            {
                if (plans[i].detailPlan != originalPlans[i].Detail)
                {
                    originalPlans[i].Detail  = plans[i].detailPlan ;

                } else {
                    Console.WriteLine("Nothing change");
                }
            }
            await _dbContext.SaveChangesAsync();
            return Ok("Updated successfully");
       }

    }
}