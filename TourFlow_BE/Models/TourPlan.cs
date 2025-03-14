using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class TourPlan
{
    public int Id { get; set; }

    public int? TourId { get; set; }

    public string? Detail { get; set; }

    public virtual Tour? Tour { get; set; }
}
