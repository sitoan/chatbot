using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class Tour
{
    public int Id { get; set; }

    public int? CityDestinationId { get; set; }

    public string? DepartureLocation { get; set; }

    public DateTime? StartDate { get; set; }

    public DateTime? EndDate { get; set; }

    public double? Price { get; set; }

    public int? AvailableSlots { get; set; }

    public virtual CityDestination? CityDestination { get; set; }

    public virtual ICollection<TourOrder> TourOrders { get; set; } = new List<TourOrder>();

    public virtual ICollection<TourPlan> TourPlans { get; set; } = new List<TourPlan>();
}
