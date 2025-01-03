
namespace TourFlowBE.ModelDtos{
        public class PutTourDto()
    {  
        public string? DepartureLocation { get; set; }

        public DateTime? StartDate { get; set; }

        public DateTime? EndDate { get; set; }

        public double? Price { get; set; }

        public int? AvailableSlots { get; set; }
        public List<UpdatePlanDto> plans { get; set; }
        public List<string> newPlans { get; set; }
    } 
}
 