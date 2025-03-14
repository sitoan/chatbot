using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace TourFlowBE.Models;

public partial class TourFlowContext : DbContext
{
    public TourFlowContext()
    {
    }

    public TourFlowContext(DbContextOptions<TourFlowContext> options)
        : base(options)
    {
    }

    public virtual DbSet<CityDestination> CityDestinations { get; set; }

    public virtual DbSet<CountryDestination> CountryDestinations { get; set; }

    public virtual DbSet<Img> Imgs { get; set; }

    public virtual DbSet<Tour> Tours { get; set; }

    public virtual DbSet<TourOrder> TourOrders { get; set; }

    public virtual DbSet<TourPlan> TourPlans { get; set; }

    public virtual DbSet<TourflowUser> TourflowUsers { get; set; }

    public virtual DbSet<UserDataCollection> UserDataCollections { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
=> optionsBuilder.UseSqlServer("Server=localhost;Database=TourFlow_CodeFirst;User Id=sa;Password=dockerStrongPwd123;TrustServerCertificate=true");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<CityDestination>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__CityDest__3214EC279EEB85A6");

            entity.ToTable("CityDestination");

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.City).HasMaxLength(1000);
            entity.Property(e => e.CountryDestinationId).HasColumnName("CountryDestinationID");

            entity.HasOne(d => d.CountryDestination).WithMany(p => p.CityDestinations)
                .HasForeignKey(d => d.CountryDestinationId)
                .OnDelete(DeleteBehavior.Cascade)
                .HasConstraintName("FK_CountryDestination");
        });

        modelBuilder.Entity<CountryDestination>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__CountryD__3214EC273AB0E1C6");

            entity.ToTable("CountryDestination");

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.Country).HasMaxLength(1000);
        });

        modelBuilder.Entity<Img>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__IMGs__3214EC270676CB0B");

            entity.ToTable("IMGs");

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.CityDestinationId).HasColumnName("CityDestinationID");
            entity.Property(e => e.Url)
                .HasMaxLength(1000)
                .IsUnicode(false);

            entity.HasOne(d => d.CityDestination).WithMany(p => p.Imgs)
                .HasForeignKey(d => d.CityDestinationId)
                .OnDelete(DeleteBehavior.Cascade)
                .HasConstraintName("FK_IMGsTourID");
        });

        modelBuilder.Entity<Tour>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Tour__3214EC2728815A36");

            entity.ToTable("Tour");

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.CityDestinationId).HasColumnName("CityDestinationID");
            entity.Property(e => e.DepartureLocation).HasMaxLength(500);
            entity.Property(e => e.EndDate).HasColumnType("datetime");
            entity.Property(e => e.StartDate).HasColumnType("datetime");

            entity.HasOne(d => d.CityDestination).WithMany(p => p.Tours)
                .HasForeignKey(d => d.CityDestinationId)
                .OnDelete(DeleteBehavior.Cascade)
                .HasConstraintName("FK_TourID");
        });

        modelBuilder.Entity<TourOrder>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__TourOrde__3214EC2712660D55");

            entity.ToTable("TourOrder", tb => tb.HasTrigger("trg_DecreaseProductQuantity"));

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.BookDate).HasColumnType("datetime");
            entity.Property(e => e.TourflowUserId).HasColumnName("TourflowUserID");

            entity.HasOne(d => d.TourBookedNavigation).WithMany(p => p.TourOrders)
                .HasForeignKey(d => d.TourBooked)
                .HasConstraintName("FK_BookedTourID");

            entity.HasOne(d => d.TourflowUser).WithMany(p => p.TourOrders)
                .HasForeignKey(d => d.TourflowUserId)
                .HasConstraintName("FK_TourflowUserID");
        });

        modelBuilder.Entity<TourPlan>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__TourPlan__3214EC275A643148");

            entity.ToTable("TourPlan");

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.TourId).HasColumnName("TourID");

            entity.HasOne(d => d.Tour).WithMany(p => p.TourPlans)
                .HasForeignKey(d => d.TourId)
                .OnDelete(DeleteBehavior.Cascade)
                .HasConstraintName("FK_TourPlanID");
        });

        modelBuilder.Entity<TourflowUser>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Tourflow__3214EC2764F2F9E4");

            entity.ToTable("TourflowUser");

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.AvatarUrl)
                .HasMaxLength(1000)
                .IsUnicode(false);
            entity.Property(e => e.Email).HasMaxLength(500);
            entity.Property(e => e.IsAdmin)
                .HasDefaultValue(false)
                .HasColumnName("isAdmin");
            entity.Property(e => e.Jwt)
                .HasMaxLength(1000)
                .HasColumnName("JWT");
            entity.Property(e => e.RefreshKey).HasMaxLength(1000);
            entity.Property(e => e.TourflowUserName).HasMaxLength(1000);
        });

        modelBuilder.Entity<UserDataCollection>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__User_Dat__3214EC2795DB0931");

            entity.ToTable("User_DataCollection");

            entity.Property(e => e.Id).HasColumnName("ID");
            entity.Property(e => e.Duration).HasMaxLength(100);
            entity.Property(e => e.EndPos).HasMaxLength(100);
            entity.Property(e => e.PhoneNumber).HasMaxLength(10);
            entity.Property(e => e.StarPos).HasMaxLength(100);
            entity.Property(e => e.TourId).HasColumnName("TourID");
            entity.Property(e => e.UserId).HasColumnName("UserID");

            entity.HasOne(d => d.User).WithMany(p => p.UserDataCollections)
                .HasForeignKey(d => d.UserId)
                .OnDelete(DeleteBehavior.Cascade)
                .HasConstraintName("FK_USerDataCollection");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
